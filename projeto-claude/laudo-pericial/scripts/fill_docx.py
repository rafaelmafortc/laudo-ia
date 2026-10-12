#!/usr/bin/env python3
"""Preenche o laudo .docx a partir de um JSON de operações, preservando o modelo do perito.

Uso:
  fill_docx.py RASCUNHO.docx OPERACOES.json SAIDA.docx            # minuta para revisão
  fill_docx.py MINUTA.docx '{}' FINAL.docx --final                # versão limpa, após revisão

Os identificadores ¶n, Cn e Tn.linha.coluna são os mostrados por extract_docx.py NO MESMO ARQUIVO.
Todas as operações usam a numeração original (o script resolve a ordem sozinho).

JSON de operações (todas as chaves são opcionais):
{
  "substituir":   {"¶197": "Texto novo.", "¶251": "Resp.: Texto.", "¶199": ["Par. 1", "Par. 2"]},
  "inserir_apos": {"¶355": ["Resp.: Não se aplica."]},
  "remover":      ["¶201", "¶203-¶213"],
  "marcar":       ["C7", "C9", "C13"],
  "desmarcar":    ["C3"],
  "tirar_amarelo": ["¶195", "¶244"],
  "trocar":       [{"p": "¶172", "de": "O reclamante", "para": "O Autor"}],
  "celulas":      {"T5.2.2": "Texto da célula", "T5.3.2": ["Par. 1", "Par. 2"]},
  "linhas_tabela": {"T3": [["27/06/2022", "Laudo médico / CRM … / “…”", "123"]]},
  "remover_linhas": ["T3.9", "T3.10"]
}

- "substituir" com lista: o 1º item substitui o parágrafo; os demais entram logo depois, com a mesma formatação.
- Texto entre **asteriscos duplos** sai em negrito.
- Parágrafo novo que começa com "Resp." copia a formatação do "Resp.:" mais próximo acima.
- Para inserir texto de corpo logo abaixo de um título (que é negrito), indique o modelo de formatação:
  "inserir_apos": {"¶229": {"modelo": "¶234", "paragrafos": ["Texto…"]}}.
- Texto inserido ou substituído recebe realce turquesa (minuta da IA), salvo com --sem-realce.
- "linhas_tabela" acrescenta linhas no fim da tabela copiando a formatação da última linha
  (ou da linha indicada: {"T3": {"modelo": 2, "linhas": [[...]]}}).
- "[PENDENTE: …]" e "[REVISAR: …]" recebem realce amarelo e negrito.
- --final: retira o turquesa e o vermelho e confere se restam amarelo, [PENDENTE]/[REVISAR] ou "Resp.:" vazio.
"""
import argparse
import copy
import json
import random
import re
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

sys.dont_write_bytecode = True  # a pasta da skill pode ser somente leitura
from laudo_docx import (MINUTA_HIGHLIGHT, PENDENTE_RE, checkboxes, ensure_docx, etree, is_red, load_document,
                        numbered_paragraphs, numbered_tables, paragraph_plain_text, parse_id, row_cells, table_rows,
                        w, w14)

XML_SPACE = "{http://www.w3.org/XML/1998/namespace}space"
RPR_ORDER = ["rStyle", "rFonts", "b", "bCs", "i", "iCs", "caps", "smallCaps", "strike", "dstrike", "outline",
             "shadow", "emboss", "imprint", "noProof", "snapToGrid", "vanish", "webHidden", "color", "spacing",
             "w", "kern", "position", "sz", "szCs", "highlight", "u", "effect", "bdr", "shd", "fitText",
             "vertAlign", "rtl", "cs", "em", "lang", "eastAsianLayout", "specVanish", "oMath"]
KEEP_IN_PARAGRAPH = {w("pPr"), w("bookmarkStart"), w("bookmarkEnd")}
TOKEN_RE = re.compile(r"(\*\*.+?\*\*|\[(?:PENDENTE|REVISAR)[^\]]*\])")


def set_rpr(rpr, tag, attrs=None):
    """Define um filho de w:rPr respeitando a ordem do esquema (o Word recusa fora de ordem)."""
    for old in rpr.findall(w(tag)):
        rpr.remove(old)
    el = etree.Element(w(tag))
    for k, v in (attrs or {}).items():
        el.set(w(k), v)
    pos = RPR_ORDER.index(tag)
    for i, child in enumerate(rpr):
        name = etree.QName(child).localname
        if name in RPR_ORDER and RPR_ORDER.index(name) > pos:
            rpr.insert(i, el)
            return
    rpr.append(el)


def drop_rpr(rpr, tag):
    for old in rpr.findall(w(tag)):
        rpr.remove(old)


def base_rpr(paragraph):
    """Formatação de caractere a herdar: a do primeiro trecho com texto, sem realce e sem vermelho."""
    source = None
    for run in paragraph.iter(w("r")):
        in_checkbox = any(a.tag == w("sdt") and a.find(f"{w('sdtPr')}/{w14('checkbox')}") is not None
                          for a in run.iterancestors())
        if not in_checkbox and (run.findtext(w("t")) or "").strip():
            source = run.find(w("rPr"))
            break
    if source is None:
        ppr = paragraph.find(w("pPr"))
        source = ppr.find(w("rPr")) if ppr is not None else None
    rpr = copy.deepcopy(source) if source is not None else etree.Element(w("rPr"))
    rpr.tag = w("rPr")
    for tag in ("highlight", "shd", "vanish", "del", "ins", "rPrChange"):
        drop_rpr(rpr, tag)
    color = rpr.find(w("color"))
    if color is not None and is_red(color.get(w("val")) or ""):
        rpr.remove(color)
    return rpr


def make_runs(text, rpr_template, mark):
    runs = []
    for token in filter(None, TOKEN_RE.split(text)):
        rpr = copy.deepcopy(rpr_template)
        if token.startswith("**") and token.endswith("**") and len(token) > 4:
            token = token[2:-2]
            set_rpr(rpr, "b")
            set_rpr(rpr, "bCs")
        if PENDENTE_RE.fullmatch(token):
            set_rpr(rpr, "b")
            set_rpr(rpr, "bCs")
            set_rpr(rpr, "highlight", {"val": "yellow"})
        elif mark:
            set_rpr(rpr, "highlight", {"val": MINUTA_HIGHLIGHT})
        run = etree.Element(w("r"))
        if len(rpr):
            run.append(rpr)
        t = etree.SubElement(run, w("t"))
        t.text = token
        t.set(XML_SPACE, "preserve")
        runs.append(run)
    return runs


def rewrite_paragraph(paragraph, text, model, mark):
    """Troca o conteúdo do parágrafo pelo texto, mantendo as propriedades de parágrafo (w:pPr)."""
    rpr = base_rpr(model)
    for child in list(paragraph):
        if child.tag not in KEEP_IN_PARAGRAPH:
            paragraph.remove(child)
    for run in make_runs(text, rpr, mark):
        paragraph.append(run)


def new_paragraph_like(model, text, mark):
    p = etree.Element(w("p"))
    ppr = model.find(w("pPr"))
    if ppr is not None:
        p.append(copy.deepcopy(ppr))
    rewrite_paragraph(p, text, model, mark)
    return p


def resp_model(paragraphs, n, fallback):
    """Para parágrafo novo que começa com 'Resp.', usa o 'Resp.:' mais próximo acima como modelo."""
    for k in range(n, 0, -1):
        if paragraph_plain_text(paragraphs[k]).strip().lower().startswith("resp"):
            return paragraphs[k]
    return fallback


def expand_ids(items):
    nums = []
    for item in items:
        if "-" in str(item):
            a, b = str(item).split("-", 1)
            nums.extend(range(parse_id(a, "¶"), parse_id(b, "¶") + 1))
        else:
            nums.append(parse_id(item, "¶"))
    return nums


def set_checkbox(sdt, checked):
    box = sdt.find(f"{w('sdtPr')}/{w14('checkbox')}")
    state = box.find(w14("checked"))
    if state is None:
        state = etree.Element(w14("checked"))
        box.insert(0, state)
    state.set(w14("val"), "1" if checked else "0")
    glyph_el = box.find(w14("checkedState" if checked else "uncheckedState"))
    glyph = chr(int(glyph_el.get(w14("val")), 16)) if glyph_el is not None else ("☒" if checked else "☐")
    texts = list(sdt.iter(w("t")))
    if texts:
        texts[0].text = glyph
        for t in texts[1:]:
            t.text = ""


def replace_in_paragraph(paragraph, old, new):
    """Troca um trecho de texto mesmo que ele atravesse vários w:t; mantém a formatação do 1º trecho."""
    nodes = list(paragraph.iter(w("t")))
    full = "".join(t.text or "" for t in nodes)
    start = full.find(old)
    if start < 0:
        return False
    end = start + len(old)
    pos = 0
    first = True
    for t in nodes:
        text = t.text or ""
        a, b = pos, pos + len(text)
        pos = b
        if b <= start or a >= end:
            continue
        cut_a, cut_b = max(start, a) - a, min(end, b) - a
        t.text = text[:cut_a] + (new if first else "") + text[cut_b:]
        t.set(XML_SPACE, "preserve")
        first = False
    return True


def fill_cell(cell, value, mark):
    """Põe o texto na célula: o 1º parágrafo vira o texto, os demais itens viram parágrafos novos."""
    texts = value if isinstance(value, list) else [value]
    paragraphs = cell.findall(w("p"))
    first = paragraphs[0] if paragraphs else etree.SubElement(cell, w("p"))
    model = copy.deepcopy(first)
    for extra in paragraphs[1:]:
        cell.remove(extra)
    rewrite_paragraph(first, texts[0], model, mark)
    anchor = first
    for text in texts[1:]:
        new = new_paragraph_like(model, text, mark)
        anchor.addnext(new)
        anchor = new


def renew_ids(element):
    """Cópia de linha não pode repetir w14:paraId/textId nem o w:id de controles de conteúdo."""
    for el in element.iter():
        for attr in (w14("paraId"), w14("textId")):
            if attr in el.attrib:
                del el.attrib[attr]
    for sdt_id in element.iter(w("id")):
        if sdt_id.getparent() is not None and sdt_id.getparent().tag == w("sdtPr"):
            sdt_id.set(w("val"), str(random.randint(10**8, 2**31 - 1)))


def parse_cell_ref(ref):
    parts = [int(x) for x in re.findall(r"\d+", str(ref))]
    if len(parts) not in (2, 3):
        raise ValueError(f"Referência de tabela inválida: {ref!r} (use T3.2 para linha ou T3.2.1 para célula)")
    return parts


def apply_table_operations(root, ops, mark, log):
    tables = numbered_tables(root)

    def table(n):
        if n not in tables:
            sys.exit(f"T{n} não existe (o documento tem {len(tables)} tabelas).")
        return tables[n]

    def row(t, k):
        rows = table_rows(table(t))
        if not 1 <= k <= len(rows):
            sys.exit(f"T{t} não tem a linha {k} (tem {len(rows)}).")
        return rows[k - 1]

    for ref, value in ops.get("celulas", {}).items():
        t, k, j = parse_cell_ref(ref)
        cells = row_cells(row(t, k))
        if not 1 <= j <= len(cells):
            sys.exit(f"T{t}.{k} não tem a coluna {j} (tem {len(cells)}).")
        fill_cell(cells[j - 1], value, mark)

    to_remove = [row(*parse_cell_ref(ref)[:2]) for ref in ops.get("remover_linhas", [])]

    for ref, spec in ops.get("linhas_tabela", {}).items():
        t = parse_id(ref, "T")
        rows = table_rows(table(t))
        model_idx = spec.get("modelo", len(rows)) if isinstance(spec, dict) else len(rows)
        new_rows = spec["linhas"] if isinstance(spec, dict) else spec
        model = row(t, model_idx)
        anchor = rows[-1]
        for values in new_rows:
            new = copy.deepcopy(model)
            renew_ids(new)
            cells = row_cells(new)
            if len(values) > len(cells):
                sys.exit(f"Linha com {len(values)} colunas para T{t}, que tem {len(cells)}.")
            for cell, value in zip(cells, list(values) + [""] * (len(cells) - len(values))):
                for drawing in list(cell.iter(w("drawing"))):
                    drawing.getparent().remove(drawing)
                fill_cell(cell, value, mark)
            anchor.addnext(new)
            anchor = new
        log.append(f"T{t}: {len(new_rows)} linha(s) acrescentada(s)")

    for r in to_remove:
        r.getparent().remove(r)
    if ops.get("celulas"):
        log.append(f"células preenchidas: {len(ops['celulas'])}")
    if to_remove:
        log.append(f"linhas de tabela removidas: {len(to_remove)}")


def apply_operations(root, ops, mark):
    paragraphs = numbered_paragraphs(root)
    boxes = checkboxes(root)
    log = []

    def para(ref):
        n = parse_id(ref, "¶")
        if n not in paragraphs:
            sys.exit(f"¶{n} não existe neste documento (o último é ¶{max(paragraphs)}).")
        return n, paragraphs[n]

    apply_table_operations(root, ops, mark, log)

    for ref in ops.get("marcar", []) + ops.get("desmarcar", []):
        k = parse_id(ref, "C")
        if not 1 <= k <= len(boxes):
            sys.exit(f"C{k} não existe (o documento tem {len(boxes)} caixas).")
    for ref in ops.get("marcar", []):
        set_checkbox(boxes[parse_id(ref, "C") - 1], True)
    for ref in ops.get("desmarcar", []):
        set_checkbox(boxes[parse_id(ref, "C") - 1], False)
    if ops.get("marcar") or ops.get("desmarcar"):
        log.append(f"caixas marcadas: {len(ops.get('marcar', []))}; desmarcadas: {len(ops.get('desmarcar', []))}")

    for item in ops.get("trocar", []):
        n, p = para(item["p"])
        if not replace_in_paragraph(p, item["de"], item["para"]):
            sys.exit(f"Em ¶{n}, o trecho {item['de']!r} não foi encontrado.")
        log.append(f"¶{n}: {item['de']!r} → {item['para']!r}")

    for ref in ops.get("tirar_amarelo", []):
        n, p = para(ref)
        for hl in p.iter(w("highlight")):
            if hl.get(w("val")) == "yellow":
                hl.getparent().remove(hl)

    removed = set(expand_ids(ops.get("remover", [])))
    replaced = {parse_id(k, "¶"): v for k, v in ops.get("substituir", {}).items()}
    inserted = {parse_id(k, "¶"): v for k, v in ops.get("inserir_apos", {}).items()}
    clash = removed & set(replaced)
    if clash:
        sys.exit(f"Os mesmos parágrafos estão em 'remover' e 'substituir': {sorted(clash)}")

    for n in sorted(set(replaced) | set(inserted)):
        _, p = para(n)
        anchor = p
        if n in replaced:
            texts = replaced[n] if isinstance(replaced[n], list) else [replaced[n]]
            model = copy.deepcopy(p)
            rewrite_paragraph(p, texts[0], model, mark)
            for text in texts[1:]:
                new = new_paragraph_like(model, text, mark)
                anchor.addnext(new)
                anchor = new
        if n in inserted:
            spec = inserted[n]
            fixed_model = None
            if isinstance(spec, dict):
                fixed_model = para(spec["modelo"])[1] if "modelo" in spec else None
                spec = spec["paragrafos"]
            texts = spec if isinstance(spec, list) else [spec]
            for text in texts:
                if fixed_model is not None:
                    model = fixed_model
                elif text.strip().lower().startswith("resp"):
                    model = resp_model(paragraphs, n, p)
                else:
                    model = p
                new = new_paragraph_like(model, text, mark)
                anchor.addnext(new)
                anchor = new
    if replaced or inserted:
        log.append(f"parágrafos substituídos: {len(replaced)}; com inserção depois: {len(inserted)}")

    for n in sorted(removed):
        _, p = para(n)
        if p.find(f"{w('pPr')}/{w('sectPr')}") is not None:
            rewrite_paragraph(p, "", p, mark=False)  # guarda a quebra de seção; só esvazia
            log.append(f"¶{n} tem quebra de seção: esvaziado em vez de removido")
            continue
        p.getparent().remove(p)
    if removed:
        log.append(f"parágrafos removidos: {len(removed)}")
    return log


def finalize(root, force):
    """Versão final: retira o turquesa da minuta e o vermelho; acusa o que ainda está pendente."""
    for hl in list(root.iter(w("highlight"))):
        if hl.get(w("val")) == MINUTA_HIGHLIGHT:
            hl.getparent().remove(hl)
    for color in list(root.iter(w("color"))):
        if color.getparent().tag == w("rPr") and is_red(color.get(w("val")) or ""):
            color.getparent().remove(color)
    problems = []
    for n, p in numbered_paragraphs(root).items():
        text = paragraph_plain_text(p)
        if any(hl.get(w("val")) == "yellow" for hl in p.iter(w("highlight"))):
            problems.append(f"¶{n} ainda tem realce amarelo: {text[:70]!r}")
        if PENDENTE_RE.search(text):
            problems.append(f"¶{n} ainda tem {PENDENTE_RE.search(text).group(0)[:70]}")
        if text.strip().rstrip(":").strip().lower() in ("resp", "resp."):
            problems.append(f"¶{n} tem 'Resp.:' sem resposta")
    if problems:
        print("ATENÇÃO, pendências na versão final:\n  " + "\n  ".join(problems))
        if not force:
            sys.exit("Versão final NÃO gerada. Resolva as pendências ou use --forcar.")
    return problems


def write_docx(source, root, output):
    tmp = Path(tempfile.mkdtemp(prefix="laudo_fill_")) / "out.docx"
    with zipfile.ZipFile(source) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "word/document.xml":
                data = etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)
            zout.writestr(item, data)
    with zipfile.ZipFile(tmp) as check:
        etree.fromstring(check.read("word/document.xml"))
    output.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(tmp), output)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("laudo", type=Path)
    parser.add_argument("operacoes", help="arquivo .json ou o próprio JSON entre aspas")
    parser.add_argument("saida", type=Path)
    parser.add_argument("--sem-realce", action="store_true", help="não marca o texto novo em turquesa")
    parser.add_argument("--final", action="store_true", help="gera a versão limpa, depois da revisão do perito")
    parser.add_argument("--forcar", action="store_true", help="com --final, gera mesmo com pendências")
    args = parser.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    raw = Path(args.operacoes).read_text(encoding="utf-8") if Path(args.operacoes).is_file() else args.operacoes
    ops = json.loads(raw)
    source = ensure_docx(args.laudo)
    root = load_document(source)

    log = apply_operations(root, ops, mark=not args.sem_realce and not args.final)
    if args.final:
        finalize(root, args.forcar)
        log.append("versão final: turquesa e vermelho retirados")
    write_docx(source, root, args.saida)
    print("\n".join(log) if log else "nenhuma operação aplicada")
    print(f"Gerado: {args.saida}")


if __name__ == "__main__":
    main()
