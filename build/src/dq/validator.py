from src.dq.rules import DataQualityRules


class DataQualityValidator:

    def validate(
        self,
        dataframe,
        dataset_name,
        required_columns,
        duplicate_column=None,
        numeric_columns=None,
    ):

        results = {
            "dataset": dataset_name,

            "row_count": len(dataframe),

            "column_count": len(dataframe.columns),

            "columns": dataframe.columns.tolist(),

            "passed": True,

            "checks": {}
        }

        # Empty dataset

        is_not_empty = DataQualityRules.check_empty(dataframe)

        results["checks"]["not_empty"] = is_not_empty

        if not is_not_empty:
            results["passed"] = False

        # Required columns

        columns_ok, missing = DataQualityRules.check_required_columns(
            dataframe,
            required_columns
        )

        results["checks"]["required_columns"] = {
            "passed": columns_ok,
            "missing": missing
        }

        if not columns_ok:
            results["passed"] = False

        # Null values

        null_results = DataQualityRules.check_nulls(
            dataframe,
            required_columns
        )

        results["checks"]["null_values"] = null_results

        for count in null_results.values():

            if count > 0:
                results["passed"] = False

        # Duplicate check

        if duplicate_column:

            duplicate_count = DataQualityRules.check_duplicates(
                dataframe,
                duplicate_column
            )

            results["checks"]["duplicates"] = duplicate_count

            if duplicate_count > 0:
                results["passed"] = False

        # Negative values

        if numeric_columns:

            negative_results = DataQualityRules.check_negative_values(
                dataframe,
                numeric_columns
            )

            results["checks"]["negative_values"] = negative_results

            for count in negative_results.values():

                if count > 0:
                    results["passed"] = False

        return results