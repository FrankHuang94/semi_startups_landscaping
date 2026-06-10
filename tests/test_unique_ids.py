from collections import Counter

from scripts.common import all_companies, all_investors, load_yaml, RESEARCH_DIR, TRANSACTION_DIR


def assert_unique(records, field):
    values = [record[field] for record in records]
    assert not [value for value, count in Counter(values).items() if count > 1]


def test_unique_ids():
    assert_unique(all_companies(), "company_id")
    assert_unique(all_investors(), "investor_id")
    assert_unique(load_yaml(RESEARCH_DIR / "papers.yaml", []), "paper_id")
    assert_unique(load_yaml(RESEARCH_DIR / "patents.yaml", []), "patent_id")
    assert_unique(load_yaml(RESEARCH_DIR / "researchers.yaml", []), "researcher_id")
    assert_unique(load_yaml(TRANSACTION_DIR / "ma_transactions.yaml", []), "transaction_id")
