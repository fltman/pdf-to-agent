#!/usr/bin/env python3
"""
PDF to Markdown Extraction Script

Extraherar text från PDF-filer och skapar LLM-optimerad markdown.

Användning:
    python extraction-script.py input.pdf output_dir/

Krav:
    pip install PyPDF2 pdfplumber
"""

import os
import sys
import re
from pathlib import Path

try:
    from PyPDF2 import PdfReader, PdfWriter
except ImportError:
    print("Installera PyPDF2: pip install PyPDF2")
    sys.exit(1)

try:
    import pdfplumber
except ImportError:
    print("Installera pdfplumber: pip install pdfplumber")
    sys.exit(1)


def split_pdf(input_pdf: str, output_dir: str) -> list[str]:
    """Splittar PDF till enskilda sidor."""
    reader = PdfReader(input_pdf)
    pages = []

    for i, page in enumerate(reader.pages):
        writer = PdfWriter()
        writer.add_page(page)

        output_path = os.path.join(output_dir, f"page_{i+1:03d}.pdf")
        with open(output_path, "wb") as f:
            writer.write(f)
        pages.append(output_path)

    print(f"Splittade {len(pages)} sidor till {output_dir}")
    return pages


def extract_text(pdf_path: str) -> tuple[str, list]:
    """Extraherar text och tabeller från en PDF-sida."""
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[0]
        text = page.extract_text() or ""
        tables = page.extract_tables() or []

    return text, tables


def clean_text(text: str) -> str:
    """Rensar text från headers, footers och onödig whitespace."""
    lines = text.split('\n')

    # Ta bort vanliga headers/footers
    skip_patterns = [
        r'^Page \d+',
        r'^\d+$',  # Bara sidnummer
        r'^Official Journal',
        r'^EN\s*$',
        r'^\s*$',
    ]

    cleaned = []
    for line in lines:
        skip = False
        for pattern in skip_patterns:
            if re.match(pattern, line.strip()):
                skip = True
                break
        if not skip:
            cleaned.append(line)

    # Ta bort överflödiga blankrader
    result = '\n'.join(cleaned)
    result = re.sub(r'\n{3,}', '\n\n', result)

    return result.strip()


def table_to_markdown(table: list) -> str:
    """Konverterar en tabell till markdown-format."""
    if not table or not table[0]:
        return ""

    # Header
    header = "| " + " | ".join(str(cell or "") for cell in table[0]) + " |"
    separator = "| " + " | ".join("---" for _ in table[0]) + " |"

    # Rows
    rows = []
    for row in table[1:]:
        rows.append("| " + " | ".join(str(cell or "") for cell in row) + " |")

    return "\n".join([header, separator] + rows)


def to_markdown(text: str, tables: list, page_num: int) -> str:
    """Konverterar text och tabeller till markdown."""
    md = f"<!-- Page {page_num} -->\n\n"

    # Lägg till text
    md += clean_text(text)

    # Lägg till tabeller
    for table in tables:
        md += "\n\n" + table_to_markdown(table)

    return md


def process_pdf(input_pdf: str, output_dir: str):
    """Processerar en PDF till markdown-filer."""
    # Skapa output-mappar
    pdf_dir = os.path.join(output_dir, "pdf_pages")
    md_dir = os.path.join(output_dir, "markdown")
    os.makedirs(pdf_dir, exist_ok=True)
    os.makedirs(md_dir, exist_ok=True)

    # Splitta PDF
    pages = split_pdf(input_pdf, pdf_dir)

    # Extrahera varje sida
    all_markdown = []
    for i, page_path in enumerate(pages):
        text, tables = extract_text(page_path)
        md = to_markdown(text, tables, i + 1)

        # Spara individuell markdown
        md_path = os.path.join(md_dir, f"page_{i+1:03d}.md")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md)

        all_markdown.append(md)
        print(f"Processade sida {i+1}/{len(pages)}")

    # Spara komplett markdown
    complete_path = os.path.join(md_dir, "COMPLETE.md")
    with open(complete_path, "w", encoding="utf-8") as f:
        f.write("\n\n---\n\n".join(all_markdown))

    print(f"\nKlart! Output i {output_dir}")
    print(f"  - {len(pages)} PDF-sidor i {pdf_dir}")
    print(f"  - {len(pages)} markdown-filer i {md_dir}")
    print(f"  - Komplett fil: {complete_path}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Användning: python extraction-script.py input.pdf output_dir/")
        sys.exit(1)

    input_pdf = sys.argv[1]
    output_dir = sys.argv[2]

    if not os.path.exists(input_pdf):
        print(f"Fel: {input_pdf} finns inte")
        sys.exit(1)

    process_pdf(input_pdf, output_dir)
