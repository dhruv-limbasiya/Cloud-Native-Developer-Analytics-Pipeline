import json
from pathlib import Path

from src.core.logger import Logger


class DataQualityReport:
    """
    Prints and saves Data Quality reports.
    """

    def __init__(self):

        self.logger = Logger.get_logger()

    def print_report(
        self,
        result
    ):

        self.logger.info("=" * 60)

        self.logger.info(
            f"Dataset : {result['dataset']}"
        )

        self.logger.info(
            f"Status  : {'PASSED' if result['passed'] else 'FAILED'}"
        )

        self.logger.info("-" * 60)

        self.logger.info(
            f"Rows    : {result['row_count']}"
        )

        self.logger.info(
            f"Columns : {result['column_count']}"
        )

        self.logger.info("-" * 60)

        for check_name, value in result["checks"].items():

            self.logger.info(
                f"{check_name} : {value}"
            )

        self.logger.info("=" * 60)

    def save_json(
        self,
        result,
        organization,
        year,
        month,
        day
    ):

        output_directory = (
            Path("logs")
            / "dq"
            / f"organization={organization}"
            / f"dataset={result['dataset']}"
            / f"year={year}"
            / f"month={month}"
            / f"day={day}"
        )

        output_directory.mkdir(
            parents=True,
            exist_ok=True
        )

        output_file = (
            output_directory
            / "report.json"
        )

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                result,
                file,
                indent=4,
                default=str
            )

        self.logger.info(
            f"Saved DQ Report -> {output_file}"
        )

        return str(output_file)