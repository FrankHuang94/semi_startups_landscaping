from scripts.common import all_companies


def test_unsourced_records_are_explicit_placeholders():
    for company in all_companies():
        if company.get("sources"):
            continue
        notes = str(company.get("data_quality", {}).get("notes", "")).lower()
        assert "placeholder" in notes or "example" in notes
