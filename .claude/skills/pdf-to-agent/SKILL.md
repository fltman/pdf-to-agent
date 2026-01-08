---
name: pdf-to-agent
description: Teknisk referens för PDF-till-agent transformation
---

# PDF to Agent Skill

## Pipeline

```
PDF → Split → Extract → Clean → Structure → Consolidate → Agent
```

## Verktyg

### PDF Split
```bash
pdftk input.pdf burst output page_%03d.pdf
```

### Text Extraction
```bash
pdftotext -layout page.pdf page.txt
```

### Python alternativ
```python
# Split
from PyPDF2 import PdfReader, PdfWriter

# Extract (med tabeller)
import pdfplumber
with pdfplumber.open("page.pdf") as pdf:
    text = pdf.pages[0].extract_text()
    tables = pdf.pages[0].extract_tables()
```

## Markdown-regler

**Ta bort:** Headers, footers, sidnummer, disclaimers

**Behåll:** Substans, definitioner, krav, siffror, tabeller

**Strukturera:**
```markdown
# Rubrik
## Sektion
- Punktlista
| Tabell | Data |
**Term**: Definition
```

## Konsolideringsmönster

| Regex | Typ | Gruppera per |
|-------|-----|--------------|
| `Article \d+` | EU-lag | Artikel |
| `Section \d+` | RFC | Sektion |
| `\d+\.\d+` | ISO | Kontroll |
| `§ \d+` | Svensk lag | Paragraf |

## Agent YAML

```yaml
---
name: namn
description: beskrivning
tools: Read, Grep, Glob, Write, Edit
model: inherit
skills: namn
---
```

## Skill YAML

```yaml
---
name: namn
description: beskrivning
---

# Titel
[Snabbreferens - max 2-3 skärmar]
```

## Filstruktur

```
output/
├── .claude/
│   ├── agents/[namn].md
│   └── skills/[namn]/SKILL.md
└── markdown/
    ├── [DOC]_COMPLETE.md
    └── [doc]_by_section/
```

## Felsökning

| Problem | Lösning |
|---------|---------|
| Skannad PDF | `tesseract` OCR |
| Trasiga tabeller | `pdfplumber` |
| Blandade kolumner | `pdftotext -layout` |
| Stora filer | Batch-processa |
