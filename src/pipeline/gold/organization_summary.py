import pandas as pd


class OrganizationSummary:

    @staticmethod
    def build(
        organization: str,
        repository_df: pd.DataFrame,
        language_df: pd.DataFrame,
        contributor_df: pd.DataFrame,
        activity_df: pd.DataFrame,
    ) -> pd.DataFrame:

        repositories = len(repository_df)

        contributors = contributor_df["contributor_count"].sum()

        commits = activity_df["commit_count"].sum()

        issues = activity_df["issue_count"].sum()

        pull_requests = activity_df["pull_request_count"].sum()

        stars = repository_df["star_count"].sum()

        forks = repository_df["fork_count"].sum()

        primary_language = language_df.iloc[0]["language"] \
            if not language_df.empty else None

        return pd.DataFrame(
            [
                {
                    "organization": organization,
                    "repositories": repositories,
                    "contributors": contributors,
                    "commits": commits,
                    "issues": issues,
                    "pull_requests": pull_requests,
                    "stars": stars,
                    "forks": forks,
                    "primary_language": primary_language,
                }
            ]
        )