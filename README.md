# Semiconductor VC Landscape

A Git-native market-intelligence database for semiconductor and AI infrastructure
venture investing. YAML files are the auditable source of truth; Markdown dashboards,
CSV files, and SQLite are generated views.

The repository supports sourcing, market mapping, investment screening, technical
diligence, co-investor analysis, M&A exit analysis, and category-by-category refreshes.
Initial records are deliberately conservative placeholders and must be replaced with
source-backed research.

## Investor Workflow

1. Review [the VC dashboard](docs/vc_dashboard.md) and generated watchlists.
2. Open a category page to compare companies and diligence gaps.
3. Update source-backed YAML records through a branch and pull request.
4. Refresh the affected section, which updates metadata and derived outputs.
5. Run the full build before investment committee or periodic market reviews.

## Category Taxonomy

The 15 primary categories cover datacenter accelerators, inference, custom ASICs and
chiplets, server CPUs, memory and CXL, networking, optical interconnect, PCIe/CXL
connectivity, edge AI, automotive and robotics silicon, EDA and developer tools,
advanced packaging, RISC-V IP, confidential computing, and power/thermal infrastructure.
The canonical definitions are in `data/market_maps/category_taxonomy.yaml`.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Validate and Build

```bash
python scripts/validate_data.py
python scripts/generate_schemas.py
python scripts/generate_docs.py
python scripts/generate_watchlists.py
python scripts/export_to_csv.py
python scripts/export_to_sqlite.py
python scripts/build_all.py
```

## Add or Update a Company

Create a YAML file containing one complete company record, then run:

```bash
python scripts/add_company.py \
  --section datacenter_ai_accelerators \
  --input /path/to/company.yaml

python scripts/update_company.py \
  --company-id company_slug_001 \
  --input /path/to/company.yaml
```

Every non-placeholder company needs at least one source. Unknown funding, customers,
benchmarks, revenue, and valuations must remain `null`.

## Refresh a Section

View current records:

```bash
python scripts/refresh_section.py \
  --section datacenter_ai_accelerators \
  --mode full \
  --list
```

Apply a structured operation file:

```yaml
add: []
update: []
remove: []
archive: []
```

```bash
python scripts/refresh_section.py \
  --section datacenter_ai_accelerators \
  --mode full \
  --operations /path/to/operations.yaml \
  --summary "Quarterly market refresh"

python scripts/refresh_section.py --section research_papers --mode targeted
python scripts/refresh_section.py --section patents --mode targeted
```

The refresh command validates data, regenerates documentation and watchlists, and
updates CSV and SQLite exports.

## Add Papers, Patents, and Researchers

Add records to `data/research/papers.yaml`, `patents.yaml`, or `researchers.yaml` using
the matching JSON schema. Link records through stable IDs and include primary paper or
patent-office sources. Update `emerging_research_themes.yaml` when multiple records
support a broader commercialization thesis.

## Founder Radar

Researcher profiles should use evidence such as repeated top-tier publications, patent
activity, open-source adoption, industry collaboration, grants, and startup history.
Run `python scripts/generate_watchlists.py` to rebuild founder and research opportunity
views.

## Exports

CSV exports are written to `exports/`. SQLite is written to
`exports/semiconductor_vc_landscape.sqlite` with normalized tables plus raw JSON fields
for analytical flexibility.

## Pull Request Review

Use a focused branch, explain source additions and scoring changes, run
`python scripts/build_all.py`, and submit a pull request. CI rejects invalid records,
duplicate IDs, missing refresh metadata, and unsourced non-placeholder records.

See [CONTRIBUTING.md](CONTRIBUTING.md), [DATA_QUALITY_POLICY.md](DATA_QUALITY_POLICY.md),
and [INVESTMENT_FRAMEWORK.md](INVESTMENT_FRAMEWORK.md).
