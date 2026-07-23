from src.transform.base_transformer import BaseTransformer


class IssuesTransformer(BaseTransformer):
    """
    Transform GitHub issues response.
    """

    def transform(
        self,
        repository_name,
        data
    ):

        records = []

        for issue in data:

            user = issue.get("user", {})

            records.append(
                {
                    "repository_name": repository_name,

                    "issue_id": issue.get("id"),

                    "issue_number": issue.get("number"),

                    "issue_title": issue.get("title"),

                    "issue_state": issue.get("state"),

                    "issue_comments": issue.get("comments"),

                    "issue_created_at": issue.get("created_at"),

                    "issue_updated_at": issue.get("updated_at"),

                    "issue_closed_at": issue.get("closed_at"),

                    "user_login": user.get("login"),

                    "is_pull_request": (
                        "pull_request" in issue
                    )
                }
            )

        dataframe = self.to_dataframe(records)

        dataframe = self.convert_datetime(
            dataframe,
            [
                "issue_created_at",
                "issue_updated_at",
                "issue_closed_at"
            ]
        )

        dataframe = self.fill_nulls(
            dataframe
        )

        return dataframe