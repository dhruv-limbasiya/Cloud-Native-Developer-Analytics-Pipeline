import pandas as pd


class RepositoryMetrics:

    @staticmethod
    def build(dataframe: pd.DataFrame) -> pd.DataFrame:

        columns = [
            "repository_id",
            "repository_name",
            "repository_full_name",
            "owner",
            "language",
            "star_count",
            "fork_count",
            "watcher_count",
            "open_issue_count",
            "size",
            "visibility",
            "created_at",
            "updated_at",
            "pushed_at"
        ]

        return dataframe[columns].copy()