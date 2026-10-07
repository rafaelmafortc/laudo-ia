#!/usr/bin/env python3
"""Extract a .docx laudo as plain text, tagging yellow-highlighted and red runs and listing images."""
import argparse
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
A = "http://schemas.openxmlformats.org/drawingml/2006/main"
PKG_REL = "http://schemas.openxmlformats.org/package/2006/relationships"
RED_COLORS = {"FF0000", "EE0000", "C00000"}


def w(tag):
    return f"{{{W}}}{tag}"


def run_marker(run):
    rpr = run.find(w("rPr"))
    if rpr is None:
        return None
    highlight = rpr.find(w("highlight"))
    if highlight is not None and highlight.get(w("val")) == "yellow":
        return "AMARELO"
    color = rpr.find(w("color"))
    if color is not None and (color.get(w("val")) or "").upper() in RED_COLORS:
        return "VERMELHO"
    return None


def run_text(run, images):
    parts = []
    for node in run.iter():
        if node.tag == w("t"):
            parts.append(node.text or "")
        elif node.tag == w("tab"):
            parts.append("\t")
        elif node.tag in (w("br"), w("cr")):
            parts.append("\n")
        elif node.tag == f"{{{A}}}blip":
            parts.append(f"[IMAGEM: {images.get(node.get(f'{{{R}}}embed'), '?')}]")
    return "".join(parts)


def paragraph_text(paragraph, images):
    segments = []
    for run in paragraph.iter(w("r")):
        text = run_text(run, images)
        if not text:
            continue
        marker = run_marker(run)
        if segments and segments[-1][0] == marker:
            segments[-1][1] += text
        else:
            segments.append([marker, text])
    return "".join(f"[{m}]{t}[/{m}]" if m and t.strip() else t for m, t in segments).strip()


def table_lines(table, images):
    lines = []
    for row in table.iter(w("tr")):
        cells = [" / ".join(filter(None, (paragraph_text(p, images) for p in cell.iter(w("p")))))
                 for cell in row.iter(w("tc"))]
        if any(cells):
            lines.append("| " + " | ".join(cells) + " |")
    return lines


def image_targets(docx, images_dir):
    rels = ET.fromstring(docx.read("word/_rels/document.xml.rels"))
    images = {}
    for rel in rels.iter(f"{{{PKG_REL}}}Relationship"):
        target = rel.get("Target")
        if not rel.get("Type", "").endswith("/image"):
            continue
        name = Path(target).name
        if images_dir:
            (images_dir / name).write_bytes(docx.read(f"word/{target}"))
            name = str(images_dir / name)
        images[rel.get("Id")] = name
    return images


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("docx", type=Path)
    parser.add_argument("--images", type=Path, help="directory to extract embedded images into")
    args = parser.parse_args()

    if args.docx.suffix.lower() != ".docx":
        sys.exit(f"Converta para .docx antes (macOS: textutil -convert docx \"{args.docx}\").")
    if args.images:
        args.images.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(args.docx) as docx:
        images = image_targets(docx, args.images)
        body = ET.fromstring(docx.read("word/document.xml")).find(w("body"))

    for block in body:
        if block.tag == w("p"):
            text = paragraph_text(block, images)
            if text:
                print(text)
        elif block.tag == w("tbl"):
            print("\n".join(table_lines(block, images)))


if __name__ == "__main__":
    main()
