# Vocabulary collection

The **top-level `vocabulary/`** directory is the canonical store for French words and expressions. It is intended to support later generation of Anki CSV files, but **no CSV files are generated until requested**.

## Current data
[entries.md](entries.md) — one Markdown table with one row per distinct vocabulary item.

| Column | Meaning |
| --- | --- |
| id | Stable unique ID, e.g. `fr-0001` |
| french | French word/expression; include an article for nouns |
| english | Concise English translation |
| example_fr | Natural French example |
| example_en | English translation of example |
| tags | Level and topical tags |
| source | Lesson or material in which the item appeared |
| notes | Gender, verb prepositions, usage, or other helpful observations |

Keep IDs stable; avoid duplicates. Preserve accents and write valid Markdown table cells (escape internal pipe characters). Future CSV exporters should validate UTF-8 and quote fields correctly.

Do not add comparisons to Spanish.
