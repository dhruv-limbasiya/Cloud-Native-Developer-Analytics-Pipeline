import pandas as pd

from src.transform.repositories_transformer import RepositoriesTransformer


def test_repository_transformer():

    transformer = RepositoriesTransformer()

    sample_data = [
        {
            "id": 1,
            "node_id": "abc123",
            "name": "tensorflow",
            "full_name": "tensorflow/tensorflow",
            "owner": {
                "login": "tensorflow"
            },
            "private": False,
            "description": "Machine Learning Framework",
            "default_branch": "master",
            "language": "Python",
            "license": {
                "spdx_id": "Apache-2.0"
            },
            "fork": False,
            "forks_count": 2500,
            "stargazers_count": 5000,
            "watchers_count": 5000,
            "open_issues_count": 150,
            "size": 1000,
            "visibility": "public",
            "created_at": "2024-01-01T10:00:00Z",
            "updated_at": "2024-01-02T10:00:00Z",
            "pushed_at": "2024-01-03T10:00:00Z"
        }
    ]

    df = transformer.transform(
        "repositories",
        sample_data
    )

    assert len(df) == 1

    assert df.loc[0, "repository_name"] == "tensorflow"

    assert df.loc[0, "owner"] == "tensorflow"

    assert df.loc[0, "license"] == "Apache-2.0"

    assert df.loc[0, "star_count"] == 5000

    assert df.loc[0, "fork_count"] == 2500

    assert df.loc[0, "watcher_count"] == 5000

    assert df.loc[0, "open_issue_count"] == 150