from datetime import datetime

from src.core.logger import Logger
from src.storage.s3_client import S3Client


class SilverWriter:

    def __init__(self):

        self.logger = Logger.get_logger()
        self.s3 = S3Client()

    def save(
        self,
        organization,
        dataset,
        dataframe,
        year,
        month,
        day
    ):

        key = (
            f"silver/"
            f"organization={organization}/"
            f"dataset={dataset}/"
            f"year={year}/"
            f"month={month}/"
            f"day={day}/"
            f"{dataset}.parquet"
        )

        s3_path = self.s3.upload_parquet(
            dataframe=dataframe,
            key=key
        )

        self.logger.info(
            f"Saved Silver Dataset -> {s3_path}"
        )

        return s3_path