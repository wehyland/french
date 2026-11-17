# Vocabulary collection (canonical source)

The top-level `vocabulary/` directory stores French vocabulary for **eventual Anki CSV export**. All records are human-readable Markdown; do not export or commit CSV files until requested.

## Current file
[entries.md](entries.md): one row per vocabulary entry in a consistent Markdown table. Additional files may be introduced if the table becomes unwieldy, provided every ID stays unique.

## Schema

| Field | Purpose |
| --- | --- |
| id | Permanent unique key, e.g. `fr-0001` |
| french | Canonical French expression; nouns include indefinite article, e.g. `un livre` |
| english | Short English meaning |
| example_fr | Natural French sentence |
| example_en | Translation of the example |
| tags | **Comma-separated**, normalized tags without embedded commas, e.g. `a1,noun,articles` |
| source | Stable source identifier, e.g. `a1-01` |
| notes | Gender, construction, meaning, register, and cautions |

## Conventions
- One row per distinct meaning or construction worth studying; do not add a duplicate merely because it reappears.
- Learn nouns with gender/article, verbs with important prepositions, and useful multiword expressions as units.
- Maintain stable IDs permanently, including when editing an entry.
- Preserve UTF-8 accents and apostrophes; avoid raw line breaks inside table cells and escape any `|` characters.
- Use French example sentences accurate for the vocabulary item. Examples can contain structures from beyond the learner's current grammar level, but label or explain them when used for grammar exercises.
- On later Anki export, validate all eight columns, ID uniqueness, CSV quoting, and the mapping of fields onto the selected card format.
- Do not use Spanish translations or comparisons.
