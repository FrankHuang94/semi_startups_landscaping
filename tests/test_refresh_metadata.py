from semivc.models import RefreshLog
from scripts.common import METADATA_DIR, category_map, load_yaml


def test_every_category_has_refresh_metadata():
    sections = load_yaml(METADATA_DIR / "section_refresh_log.yaml", {"sections": {}})["sections"]
    expected = set(category_map()) | {"research_papers", "patents", "ma_transactions", "vc_investors"}
    assert expected <= set(sections)
    for record in sections.values():
        RefreshLog.model_validate(record)
