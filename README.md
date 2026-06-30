# PDF to Agent

[![Support me on Patreon](https://img.shields.io/badge/Patreon-Support%20my%20work-FF424D?style=flat&logo=patreon&logoColor=white)](https://www.patreon.com/AndersBjarby)

Teknisk agent för PDF-till-agent transformation. Minimal, effektiv, fokuserad på extraktionsprocessen.

## Användning

```
Transformera PDF-filerna i /path/to/pdfs/ till en agent
```

## Installation

```bash
cp -r pdf-to-agent/.claude /ditt/projekt/
```

## Struktur

```
.claude/
├── agents/
│   └── pdf-to-agent.md
└── skills/
    └── pdf-to-agent/
        ├── SKILL.md
        └── templates/
            └── extraction-script.py
```

## Pipeline

```
PDF → Split → Extract → Clean → Structure → Consolidate → Agent
```

### 1. Split
```bash
pdftk input.pdf burst output page_%03d.pdf
```

### 2. Extract
```bash
pdftotext -layout page.pdf page.txt
```

### 3. Clean
Ta bort headers, footers, sidnummer. Behåll substans.

### 4. Structure
Konvertera till markdown med rubriker, listor, tabeller.

### 5. Consolidate
Slå ihop efter dokumentstruktur (artiklar, kapitel, sektioner).

### 6. Generate
Skapa agent och skill med kunskapsreferenser.

## Verktyg

| Uppgift | Primärt | Alternativ |
|---------|---------|------------|
| Split | pdftk | PyPDF2 |
| Text | pdftotext | pdfplumber |
| Tabeller | pdfplumber | camelot |
| OCR | tesseract | - |

## Python-script

Inkluderat i `templates/extraction-script.py`:

```bash
python extraction-script.py input.pdf output_dir/
```

Kräver: `pip install PyPDF2 pdfplumber`

## Output

```
output/
├── .claude/
│   ├── agents/[namn].md
│   └── skills/[namn]/SKILL.md
└── markdown/
    ├── [DOC]_COMPLETE.md
    └── [doc]_by_section/
```

## Skillnad mot andra builders

| Agent | Fokus |
|-------|-------|
| `agent-builder` | Generell, alla dokumenttyper |
| `compliance-agent-builder` | Regelverk, checklistor |
| `pdf-to-agent` | Teknisk extraktion |

## Licens

MIT
