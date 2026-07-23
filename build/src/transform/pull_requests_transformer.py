from src.transform.base_transformer import BaseTransformer


class PullRequestsTransformer(BaseTransformer):
    """
    Transform GitHub pull requests response.
    """

    def transform(
        self,
        repository_name,
        data
    ):

        records = []

        for pull_request in data:

            user = pull_request.get("user", {})

            records.append(
                {
                    "repository_name": repository_name,

                    "pull_request_id": pull_request.get("id"),

                    "pull_request_number": pull_request.get("number"),

                    "pull_request_title": pull_request.get("title"),

                    "pull_request_state": pull_request.get("state"),

                    "user_login": user.get("login"),

                    "comments": pull_request.get("comments"),

                    "commits": pull_request.get("commits"),

                    "additions": pull_request.get("additions"),

                    "deletions": pull_request.get("deletions"),

                    "changed_files": pull_request.get("changed_files"),

                    "created_at": pull_request.get("created_at"),

                    "updated_at": pull_request.get("updated_at"),

                    "closed_at": pull_request.get("closed_at"),

                    "merged_at": pull_request.get("merged_at")
                }
            )

        dataframe = self.to_dataframe(records)

        dataframe = self.convert_datetime(
            dataframe,
            [
                "created_at",
                "updated_at",
                "closed_at",
                "merged_at"
            ]
        )

        dataframe = self.fill_nulls(
            dataframe
        )

        return dataframe