from scripts.common import all_companies, all_investors, load_yaml, RESEARCH_DIR, TRANSACTION_DIR


def test_unsourced_records_are_explicit_placeholders():
    for company in all_companies():
        if company.get("sources"):
            continue
        notes = str(company.get("data_quality", {}).get("notes", "")).lower()
        assert "placeholder" in notes or "example" in notes


def test_sources_are_auditable():
    records = [
        *all_companies(),
        *all_investors(),
        *load_yaml(RESEARCH_DIR / "papers.yaml", []),
        *load_yaml(RESEARCH_DIR / "patents.yaml", []),
        *load_yaml(RESEARCH_DIR / "researchers.yaml", []),
        *load_yaml(TRANSACTION_DIR / "ma_transactions.yaml", []),
    ]
    for record in records:
        for source in record.get("sources", []):
            assert source.get("source_id")
            assert source.get("title")
            assert str(source.get("url", "")).startswith("https://")
            assert source.get("date_accessed")
            assert source.get("source_type")
            assert source.get("reliability") in {"high", "medium", "low"}
