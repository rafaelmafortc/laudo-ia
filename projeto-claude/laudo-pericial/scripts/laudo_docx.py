"""Leitura do .docx do laudo: blocos do corpo, numeração de parágrafos (¶n) e caixas de seleção (Cn).

extract_docx.py e fill_docx.py usam as mesmas funções, para que os identificadores
mostrados na extração sejam os mesmos aceitos no preenchimento.
"""
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

try:
    from lxml import etree
except ImportError:
    sys.exit("Falta a biblioteca lxml. Instale com: pip install lxml")

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
W14 = "http://schemas.microsoft.com/office/word/2010/wordml"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
A = "http://schemas.openxmlformats.org/drawingml/2006/main"
PKG_REL = "http://schemas.openxmlformats.org/package/2006/relationships"

MINUTA_HIGHLIGHT = "cyan"  # realce turquesa: texto redigido pela IA, a revisar
PENDENTE_RE = re.compile(r"\[(PENDENTE|REVISAR)[^\]]*\]")


def w(tag):
    return f"{{{W}}}{tag}"


def w14(tag):
    return f"{{{W14}}}{tag}"


def ensure_docx(path: Path) -> Path:
    """Devolve um .docx; converte .doc/.rtf/.odt com o LibreOffice, se houver."""
    if path.suffix.lower() == ".docx":
        return path
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if not soffice:
        sys.exit(f"{path.name} não é .docx e o LibreOffice não está disponível. "
                 "Abra no Word e use 'Salvar como' > .docx.")
    out_dir = Path(tempfile.mkdtemp(prefix="laudo_conv_"))
    subprocess.run([soffice, "--headless", "--convert-to", "docx", "--outdir", str(out_dir), str(path)],
                   check=True, capture_output=True, timeout=180)
    converted = out_dir / (path.stem + ".docx")
    if not converted.exists():
        sys.exit(f"A conversão de {path.name} para .docx falhou.")
    return converted


def load_document(path: Path):
    with zipfile.ZipFile(path) as docx:
        xml = docx.read("word/document.xml")
    return etree.fromstring(xml)


def body_blocks(container):
    """Percorre parágrafos e tabelas do corpo, abrindo controles de conteúdo de bloco (w:sdt)."""
    for child in container:
        if child.tag in (w("p"), w("tbl")):
            yield child
        elif child.tag == w("sdt"):
            content = child.find(w("sdtContent"))
            if content is not None:
                yield from body_blocks(content)


def numbered_paragraphs(root):
    """Mapa {n: w:p} dos parágrafos do corpo (fora de tabelas), na ordem do documento."""
    body = root.find(w("body"))
    paragraphs = [b for b in body_blocks(body) if b.tag == w("p")]
    return {i: p for i, p in enumerate(paragraphs, start=1)}


def numbered_tables(root):
    """Mapa {n: w:tbl} das tabelas do corpo (sem as aninhadas), na ordem do documento."""
    body = root.find(w("body"))
    tables = [b for b in body_blocks(body) if b.tag == w("tbl")]
    return {i: t for i, t in enumerate(tables, start=1)}


def table_rows(table):
    return table.findall(w("tr"))


def row_cells(row):
    cells = []
    for child in row:
        if child.tag == w("tc"):
            cells.append(child)
        elif child.tag == w("sdt"):
            cells.extend(child.iter(w("tc")))
    return cells


def checkboxes(root):
    """Lista de w:sdt que são caixas de seleção (w14:checkbox), na ordem do documento."""
    return [sdt for sdt in root.iter(w("sdt"))
            if sdt.find(f"{w('sdtPr')}/{w14('checkbox')}") is not None]


def checkbox_checked(sdt):
    checked = sdt.find(f"{w('sdtPr')}/{w14('checkbox')}/{w14('checked')}")
    return checked is not None and checked.get(w14("val")) in ("1", "true")


def paragraph_plain_text(p):
    return "".join(t.text or "" for t in p.iter(w("t")))


def parse_id(value: str, prefix: str) -> int:
    """Aceita '¶12', 'P12', '12' (parágrafo) ou 'C3', '3' (caixa)."""
    digits = re.sub(r"\D", "", str(value))
    if not digits:
        raise ValueError(f"Identificador inválido: {value!r} (esperado {prefix}<número>)")
    return int(digits)


def is_red(color_val: str) -> bool:
    if not color_val or not re.fullmatch(r"[0-9A-Fa-f]{6}", color_val):
        return False
    r, g, b = (int(color_val[i:i + 2], 16) for i in (0, 2, 4))
    return r >= 0xB0 and g <= 0x50 and b <= 0x50
