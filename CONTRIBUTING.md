# Contributing

## Change Discipline

- Treat YAML under `data/` as the source of truth.
- Use stable lowercase IDs; never recycle an ID for another entity.
- Keep unknown facts as `null`.
- Cite non-obvious claims and distinguish company claims from independent verification.
- Update the relevant section refresh log and `CHANGELOG.md`.
- Do not hand-edit generated docs, CSV files, or SQLite outputs.

## Company Changes

Use `scripts/add_company.py` and `scripts/update_company.py` for individual records, or
`scripts/refresh_section.py` for a category refresh. A company move between categories
should be reviewed as an explicit remove and add operation.

## Research and Transaction Changes

Use canonical paper, patent, researcher, investor, and transaction IDs. Link related
entities by ID rather than by unstructured prose where possible.

## Pull Request Checklist

- Sources are accessible and correctly typed.
- Dates use `YYYY-MM-DD`.
- Scores are 1-5 and have supporting rationale.
- Rumors and estimates are explicitly labeled.
- Refresh metadata reflects the actual scope.
- `python scripts/build_all.py` passes.
