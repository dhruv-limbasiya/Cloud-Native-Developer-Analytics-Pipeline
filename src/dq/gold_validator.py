from src.core.logger import Logger
from src.dq.validator import DataQualityValidator


class GoldValidator:
    """
    Validate Gold datasets before writing.
    """

    def __init__(self):

        self.logger = Logger.get_logger()

        self.validator = DataQualityValidator()

    def validate(
        self,
        dataframe,
        dataset_name,
        required_columns,
        duplicate_column=None,
        numeric_columns=None
    ):

        self.logger.info(
            f"Validating Gold dataset: {dataset_name}"
        )

        report = self.validator.validate(
            dataframe=dataframe,
            dataset_name=dataset_name,
            required_columns=required_columns,
            duplicate_column=duplicate_column,
            numeric_columns=numeric_columns
        )

        if report["passed"]:

            self.logger.info(
                f"Gold validation passed: {dataset_name}"
            )

        else:

            self.logger.error(
                f"Gold validation failed: {dataset_name}"
            )

        return report