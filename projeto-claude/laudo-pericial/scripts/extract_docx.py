#!/usr/bin/env python3
"""Extrai o laudo (.docx, ou .doc via LibreOffice) como texto anotado.

Marcações na saída:
  ¶n            número do parágrafo do corpo (usado pelo fill_docx.py)
  {Cn}☐ / {Cn}☒  caixa de seleção n, desmarcada / marcada
  [AMARELO]…[/AMARELO]    realce amarelo (seção ou campo a preencher)
  [VERMELHO]…[/VERMELHO]  fonte vermelha (dado do caso inserido no modelo)
  [MINUTA]…[/MINUTA]      realce turquesa (texto já redigido pela IA, a revisar)
  [REALCE-cor]…           outro realce
  [IMAGEM: caminho]       imagem embutida (salva com --images)
  [Tn]                    início da tabela n
  Lk| a | b |             linha k da tabela (células por |, parágrafos da célula por /)
                          a célula da linha k, coluna j, da tabela n é "Tn.k.j"
No fim, um RESUMO com o que falta preencher.
"""
import argparse
import sys
import zipfile
from pathlib import Path

sys.dont_write_bytecode = True  # a pasta da skill pode ser somente leitura
from laudo_docx import (A, MINUTA_HIGHLIGHT, PENDENTE_RE, PKG_REL, R, body_blocks, checkbox_checked,
                        checkboxes, ensure_docx, etree, is_red, load_document, row_cells, table_rows, w)

VML_IMAGEDATA = "{urn:schemas-microsoft-com:vml}imagedata"


def run_marker(run):
    rpr = run.find(w("rPr"))
    if rpr is None:
        return None
    highlight = rpr.find(w("highlight"))
    if highlight is not None and highlight.get(w("val")) not in (None, "none"):
        val = highlight.get(w("val"))
        if val == "yellow":
            return "AMARELO"
        if val == MINUTA_HIGHLIGHT:
            return "MINUTA"
        return f"REALCE-{val}"
    shd = rpr.find(w("shd"))
    if shd is not None and (shd.get(w("fill")) or "").upper() == "FFFF00":
        return "AMARELO"
    color = rpr.find(w("color"))
    if color is not None and is_red(color.get(w("val")) or ""):
        return "VERMELHO"
    return None


class Extractor:
    def __init__(self, root, images):
        self.images = images
        self.checkbox_of_text = {}
        self.checkbox_states = []
        for n, sdt in enumerate(checkboxes(root), start=1):
            self.checkbox_states.append(checkbox_checked(sdt))
            for t in sdt.iter(w("t")):
                self.checkbox_of_text[t] = n

    def run_text(self, run):
        parts = []
        for node in run.iter():
            if node.tag == w("t"):
                n = self.checkbox_of_text.get(node)
                parts.append(f"{{C{n}}}{node.text or ''}" if n else (node.text or ""))
            elif node.tag == w("tab"):
                parts.append("\t")
            elif node.tag in (w("br"), w("cr")):
                parts.append("\n")
            elif node.tag == f"{{{A}}}blip":
                parts.append(f"[IMAGEM: {self.images.get(node.get(f'{{{R}}}embed'), '?')}]")
            elif node.tag == VML_IMAGEDATA:
                parts.append(f"[IMAGEM: {self.images.get(node.get(f'{{{R}}}id'), '?')}]")
        return "".join(parts)

    def paragraph_text(self, paragraph):
        segments = []
        for run in paragraph.iter(w("r")):
            text = self.run_text(run)
            if not text:
                continue
            marker = run_marker(run)
            if segments and segments[-1][0] == marker:
                segments[-1][1] += text
            else:
                segments.append([marker, text])
        return "".join(f"[{m}]{t}[/{m}]" if m and t.strip() else t for m, t in segments).strip()

    def table_lines(self, number, table):
        lines = [f"[T{number}]"]
        for k, row in enumerate(table_rows(table), start=1):
            cells = [" / ".join(filter(None, (self.paragraph_text(p) for p in cell.iter(w("p")))))
                     for cell in row_cells(row)]
            if any(cells):
                lines.append(f"L{k}| " + " | ".join(cells) + " |")
        return lines


def image_targets(docx, images_dir):
    rels = etree.fromstring(docx.read("word/_rels/document.xml.rels"))
    images = {}
    for rel in rels.iter(f"{{{PKG_REL}}}Relationship"):
        if not rel.get("Type", "").endswith("/image") or rel.get("TargetMode") == "External":
            continue
        target = rel.get("Target")
        name = Path(target).name
        if images_dir:
            member = target.lstrip("/") if target.startswith("/") else f"word/{target}"
            (images_dir / name).write_bytes(docx.read(member))
            name = str(images_dir / name)
        images[rel.get("Id")] = name
    return images


def ids(nums):
    return ", ".join(f"¶{n}" for n in nums) if nums else "nenhum"


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("laudo", type=Path)
    parser.add_argument("--images", type=Path, help="pasta para salvar as imagens embutidas")
    args = parser.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    source = ensure_docx(args.laudo)
    if args.images:
        args.images.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(source) as docx:
        images = image_targets(docx, args.images)
    root = load_document(source)
    ex = Extractor(root, images)

    yellow, red, minuta, pending, empty_resp = [], [], [], [], []
    n = t = 0
    for block in body_blocks(root.find(w("body"))):
        if block.tag == w("tbl"):
            t += 1
            print("\n".join(ex.table_lines(t, block)))
            continue
        n += 1
        text = ex.paragraph_text(block)
        if not text:
            continue
        print(f"¶{n} {text}")
        if "[AMARELO]" in text:
            yellow.append(n)
        if "[VERMELHO]" in text:
            red.append(n)
        if "[MINUTA]" in text:
            minuta.append(n)
        if PENDENTE_RE.search(text):
            pending.append(n)
        bare = PENDENTE_RE.sub("", text)
        for tag in ("AMARELO", "VERMELHO", "MINUTA"):
            bare = bare.replace(f"[{tag}]", "").replace(f"[/{tag}]", "")
        if bare.strip().rstrip(":").strip().lower() in ("resp", "resp.", "resposta"):
            empty_resp.append(n)

    states = ex.checkbox_states
    print("\n=== RESUMO ===")
    print(f"Arquivo: {args.laudo.name}" + (" (convertido para .docx)" if source != args.laudo else ""))
    print(f"Parágrafos com amarelo ({len(yellow)}): {ids(yellow)}")
    print(f"Parágrafos com vermelho: {len(red)}")
    print(f"'Resp.:' vazios ({len(empty_resp)}): {ids(empty_resp)}")
    print(f"Caixas de seleção: {len(states)} (marcadas: "
          f"{', '.join(f'C{i}' for i, s in enumerate(states, 1) if s) or 'nenhuma'})")
    if minuta:
        print(f"Texto de minuta (turquesa) ({len(minuta)}): {ids(minuta)}")
    if pending:
        print(f"[PENDENTE]/[REVISAR] ({len(pending)}): {ids(pending)}")
    print(f"Imagens: {len(images)}" + (f" (salvas em {args.images})" if args.images else ""))


if __name__ == "__main__":
    main()
