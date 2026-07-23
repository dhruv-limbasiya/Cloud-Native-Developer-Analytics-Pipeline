import pandas as pd


class ContributorMetrics:

    @staticmethod
    def build(dataframe: pd.DataFrame) -> pd.DataFrame:

        result = (
            dataframe
            .groupby("repository_name", as_index=False)
            .agg(
                contributor_count=(
                    "contributor_id",
                    "nunique"
                ),
                total_contributions=(
                    "contributions",
                    "sum"
                ),
                average_contributions=(
                    "contributions",
                    "mean"
                )
            )
            .sort_values(
                by="total_contributions",
                ascending=False
            )
        )

        result["average_contributions"] = (
            result["average_contributions"]
            .round(2)
        )

        return result