import pandas as pd


class LanguageMetrics:

    @staticmethod
    def build(dataframe: pd.DataFrame) -> pd.DataFrame:

        result = (
            dataframe
            .groupby("language", as_index=False)
            .agg(
                repository_count=(
                    "repository_name",
                    "nunique"
                ),
                total_bytes_of_code=(
                    "bytes_of_code",
                    "sum"
                ),
                average_bytes_per_repository=(
                    "bytes_of_code",
                    "mean"
                )
            )
            .sort_values(
                by="total_bytes_of_code",
                ascending=False
            )
        )

        result["average_bytes_per_repository"] = (
            result["average_bytes_per_repository"]
            .round(2)
        )

        return result