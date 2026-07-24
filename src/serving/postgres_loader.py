from src.core.logger import Logger

from src.storage.parquet_reader import ParquetReader
from src.serving.postgres_writer import PostgresWriter


class PostgresLoader:
    """
    Loads Gold datasets from S3
    into PostgreSQL.
    """

    def __init__(self):

        self.logger = Logger.get_logger()

        self.reader = ParquetReader()

        self.writer = PostgresWriter()

    def run(self, organization):

        self.logger.info("=" * 60)
        self.logger.info("Loading Gold Datasets into PostgreSQL")
        self.logger.info("=" * 60)

        datasets = [
            "repository_metrics",
            "language_metrics",
            "contributor_metrics",
            "repository_activity",
            "organization_summary",
        ]

        for dataset in datasets:

            prefix = (
                f"gold/"
                f"organization={organization}/"
                f"dataset={dataset}/"
            )

            files = self.reader.read_directory(prefix)

            if not files:

                self.logger.warning(
                    f"{dataset} not found."
                )

                continue

            dataframe = files[0]["data"]

            self.writer.save(
                dataframe,
                dataset,
            )

        self.logger.info("=" * 60)
        self.logger.info("PostgreSQL Loading Completed")
        self.logger.info("=" * 60)