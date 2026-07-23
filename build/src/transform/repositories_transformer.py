from src.transform.base_transformer import BaseTransformer


class RepositoriesTransformer(BaseTransformer):
    """
    Clean repository dataset.
    """

    def transform(
        self,
        repository_name,
        data
    ):

        dataframe = self.to_dataframe(data)

        dataframe["owner"] = dataframe["owner"].apply(
            lambda owner: owner.get("login")
            if isinstance(owner, dict)
            else None
        )

        dataframe["license"] = dataframe["license"].apply(
            lambda license_info: (
                license_info.get("spdx_id")
                if isinstance(license_info, dict)
                else None
            )
        )

        dataframe = self.convert_datetime(
            dataframe,
            [
                "created_at",
                "updated_at",
                "pushed_at"
            ]
        )

        dataframe = self.select_columns(
            dataframe,
            [
                "id",
                "node_id",
                "name",
                "full_name",
                "owner",
                "private",
                "description",
                "default_branch",
                "language",
                "license",
                "fork",
                "forks_count",
                "stargazers_count",
                "watchers_count",
                "open_issues_count",
                "size",
                "visibility",
                "created_at",
                "updated_at",
                "pushed_at"
            ]
        )

        dataframe = self.rename_columns(
            dataframe,
            {
                "id": "repository_id",
                "name": "repository_name",
                "full_name": "repository_full_name",
                "private": "is_private",
                "fork": "is_fork",
                "forks_count": "fork_count",
                "stargazers_count": "star_count",
                "watchers_count": "watcher_count",
                "open_issues_count": "open_issue_count"
            }
        )

        dataframe = self.fill_nulls(
            dataframe
        )

        return dataframe