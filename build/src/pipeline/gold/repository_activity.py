import pandas as pd


class RepositoryActivity:

    @staticmethod
    def build(
        commits_df: pd.DataFrame,
        issues_df: pd.DataFrame,
        pull_requests_df: pd.DataFrame
    ) -> pd.DataFrame:

        commit_metrics = (
            commits_df
            .groupby("repository_name", as_index=False)
            .agg(
                commit_count=("commit_sha", "count")
            )
        )

        issue_metrics = (
            issues_df
            .groupby("repository_name", as_index=False)
            .agg(
                issue_count=("issue_id", "count")
            )
        )

        pr_metrics = (
            pull_requests_df
            .groupby("repository_name", as_index=False)
            .agg(
                pull_request_count=("pull_request_id", "count")
            )
        )

        activity = (
            commit_metrics
            .merge(
                issue_metrics,
                on="repository_name",
                how="outer"
            )
            .merge(
                pr_metrics,
                on="repository_name",
                how="outer"
            )
            .fillna(0)
        )

        activity["commit_count"] = activity["commit_count"].astype(int)
        activity["issue_count"] = activity["issue_count"].astype(int)
        activity["pull_request_count"] = activity["pull_request_count"].astype(int)

        activity["total_activity"] = (
            activity["commit_count"]
            + activity["issue_count"]
            + activity["pull_request_count"]
        )

        activity = activity.sort_values(
            by="total_activity",
            ascending=False
        )

        return activity