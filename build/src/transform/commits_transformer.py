from src.transform.base_transformer import BaseTransformer


class CommitsTransformer(BaseTransformer):
    """
    Transform GitHub commits response.
    """

    def transform(
        self,
        repository_name,
        data
    ):

        records = []

        for commit in data:

            commit_author = commit.get("commit", {}).get("author", {})

            github_author = commit.get("author")

            records.append(
                {
                    "repository_name": repository_name,

                    "commit_sha": commit.get("sha"),

                    "author_login": (
                        github_author.get("login")
                        if github_author
                        else None
                    ),

                    "author_name": commit_author.get("name"),

                    "author_email": commit_author.get("email"),

                    "commit_date": commit_author.get("date"),

                    "commit_message": commit.get("commit", {}).get("message")
                }
            )

        dataframe = self.to_dataframe(records)

        dataframe = self.convert_datetime(
            dataframe,
            [
                "commit_date"
            ]
        )

        dataframe = self.fill_nulls(dataframe)

        return dataframe