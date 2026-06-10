from semivc.models import Company, Investor, Paper, Patent, Researcher, Transaction
from scripts.common import (
    RESEARCH_DIR,
    TRANSACTION_DIR,
    all_companies,
    all_investors,
    load_yaml,
)


def test_required_records_parse():
    for record in all_companies():
        Company.model_validate(record)
    for record in all_investors():
        Investor.model_validate(record)
    for model, path in (
        (Paper, RESEARCH_DIR / "papers.yaml"),
        (Patent, RESEARCH_DIR / "patents.yaml"),
        (Researcher, RESEARCH_DIR / "researchers.yaml"),
        (Transaction, TRANSACTION_DIR / "ma_transactions.yaml"),
    ):
        for record in load_yaml(path, []):
            model.model_validate(record)
