from pathlib import Path

import pandas as pd

from src.core.logger import Logger
from src.storage.bronze_reader import BronzeReader
from src.storage.metadata_writer import MetadataWriter
from src.storage.silver_writer import SilverWriter
from src.transform.transformer_factory import TransformerFactory

from src.dq.config import DQ_CONFIG
from src.dq.validator import DataQualityValidator
from src.dq.report import DataQualityReport


class SilverPipeline:
    """
    Bronze -> Silver Pipeline
    """

    def __init__(self):

        self.logger = Logger.get_logger()

        self.reader = BronzeReader()

        self.writer = SilverWriter()

        self.metadata = MetadataWriter()

        self.transformers = TransformerFactory.get_transformers()

        self.validator = DataQualityValidator()

        self.reporter = DataQualityReport()

    def run(
        self,
        organization,
        datasets
    ):

        self.logger.info("Starting Silver Pipeline")

        for dataset in datasets:

            transformer = self.transformers.get(dataset)

            if transformer is None:

                self.logger.warning(
                    f"No transformer found for {dataset}"
                )

                continue

            bronze_prefix = (
                f"bronze/"
                f"organization={organization}/"
                f"endpoint={dataset}/"
            )
            bronze_files  = self.reader.read_directory(bronze_prefix)

            if not bronze_files:

                self.logger.warning(
                    f"No Bronze files found for {dataset}"
                )

                continue

            combined_dataframes = []

            for bronze_file in bronze_files:

                repository_name = Path(
                    bronze_file["file_name"]
                ).stem

                self.logger.info(
                    f"Transforming {bronze_file['file_name']}"
                )

                dataframe = transformer.transform(
                    repository_name,
                    bronze_file["data"]
                )

                combined_dataframes.append(dataframe)

            if not combined_dataframes:
                continue

            final_dataframe = pd.concat(
                combined_dataframes,
                ignore_index=True
            )

            config = DQ_CONFIG.get(dataset)

            if config is None:

                self.logger.warning(
                    f"No DQ configuration found for '{dataset}'"
                )

                continue

            result = self.validator.validate(
                dataframe=final_dataframe,
                dataset_name=dataset,
                required_columns=config["required_columns"],
                duplicate_column=config["duplicate_column"],
                numeric_columns=config["numeric_columns"]
            )

            self.reporter.print_report(result)

            # Temporary values until we extract them from the S3 key
            year_value = "2026"
            month_value = "07"
            day_value = "22"

            self.reporter.save_json(
                result=result,
                organization=organization,
                year=year_value,
                month=month_value,
                day=day_value
            )

            if not result["passed"]:

                raise ValueError(
                    f"Data Quality Validation Failed: {dataset}"
                )

            output_path = self.writer.save(
                organization=organization,
                dataset=dataset,
                dataframe=final_dataframe,
                year=year_value,
                month=month_value,
                day=day_value
            )

            self.metadata.save(
                organization=organization,
                endpoint=f"silver_{dataset}",
                record_count=len(final_dataframe),
                file_path=output_path,
                status="SUCCESS"
            )

                        

        self.logger.info("Silver Pipeline Completed")