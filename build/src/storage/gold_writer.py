from io import BytesIO

import pandas as pd

from src.core.logger import Logger
from src.storage.s3_client import S3Client


class GoldWriter:
    """
    Writes Gold datasets to Amazon S3 as Parquet files.
    """

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

        s3_key = (
            f"gold/"
            f"organization={organization}/"
            f"dataset={dataset}/"
            f"year={year}/"
            f"month={month}/"
            f"day={day}/"
            f"{dataset}.parquet"
        )

        self.s3.upload_parquet(
            dataframe=dataframe,
            key=s3_key
        )

        self.logger.info(
            f"Saved Gold Dataset -> s3://{self.s3.bucket_name}/{s3_key}"
        )

        return f"s3://{self.s3.bucket_name}/{s3_key}"