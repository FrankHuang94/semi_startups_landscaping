from scripts.validate_data import validate_repository


def test_repository_validates():
    assert validate_repository() == []
