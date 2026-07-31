import pandas as pd

from src.dq.rules import DataQualityRules


def test_check_empty():

    df = pd.DataFrame({"id": [1, 2, 3]})

    assert DataQualityRules.check_empty(df) is True


def test_check_required_columns():

    df = pd.DataFrame({
        "id": [1],
        "name": ["tensorflow"]
    })

    result, missing = DataQualityRules.check_required_columns(
        df,
        ["id", "name", "owner"]
    )

    assert result is False
    assert "owner" in missing


def test_check_duplicates():

    df = pd.DataFrame({
        "repository_id": [1, 1, 2]
    })

    duplicates = DataQualityRules.check_duplicates(
        df,
        "repository_id"
    )

    assert duplicates == 1


def test_check_negative_values():

    df = pd.DataFrame({
        "star_count": [100, -10, 50]
    })

    result = DataQualityRules.check_negative_values(
        df,
        ["star_count"]
    )

    assert result["star_count"] == 1