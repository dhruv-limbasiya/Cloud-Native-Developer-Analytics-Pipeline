import pandas as pd


class DataQualityRules:

    @staticmethod
    def check_empty(dataframe):

        return len(dataframe) > 0

    @staticmethod
    def check_required_columns(
        dataframe,
        required_columns
    ):

        missing = []

        for column in required_columns:

            if column not in dataframe.columns:
                missing.append(column)

        return len(missing) == 0, missing

    @staticmethod
    def check_nulls(
        dataframe,
        columns
    ):

        results = {}

        for column in columns:

            results[column] = int(
                dataframe[column].isna().sum()
            )

        return results

    @staticmethod
    def check_duplicates(dataframe, column):

        duplicate_rows = dataframe[
            dataframe.duplicated(subset=[column], keep=False)
        ]

        print("\n================ DUPLICATE DEBUG ================")
        print("Checking column:", column)
        print("Rows:", len(dataframe))
        print("Duplicate count:", duplicate_rows.shape[0])

        if not duplicate_rows.empty:
            print(duplicate_rows)

        print("=================================================\n")

        return int(
            dataframe.duplicated(subset=[column]).sum()
        )

    @staticmethod
    @staticmethod
    def check_negative_values(
        dataframe,
        columns
    ):

        results = {}

        for column in columns:

            if column in dataframe.columns:

                numeric_series = pd.to_numeric(
                    dataframe[column],
                    errors="coerce"
                )

                results[column] = int(
                    (numeric_series < 0).sum()
                )
        return results