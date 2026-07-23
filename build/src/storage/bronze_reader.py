from datetime import datetime

from src.core.logger import Logger
from src.storage.s3_client import S3Client


class BronzeReader:
    """
    Reads the latest Bronze snapshot from S3.

    Bronze/
        organization=...
            endpoint=...
                year=2026/
                    month=07/
                        day=23/
    """

    def __init__(self):

        self.logger = Logger.get_logger()
        self.s3 = S3Client()

    def read_directory(self, prefix):

        keys = self.s3.list_objects(prefix)

        if not keys:
            return []

        latest_key = self._get_latest_key(keys)

        self.logger.info(f"Reading latest Bronze snapshot: {latest_key}")

        data = self.s3.download_json(latest_key)

        return [
            {
                "file_name": latest_key.split("/")[-1],
                "data": data,
            }
        ]

    def _get_latest_key(self, keys):

        def extract_date(key):

            parts = key.split("/")

            year = None
            month = None
            day = None

            for part in parts:

                if part.startswith("year="):
                    year = int(part.split("=")[1])

                elif part.startswith("month="):
                    month = int(part.split("=")[1])

                elif part.startswith("day="):
                    day = int(part.split("=")[1])

            return datetime(year, month, day)

        return max(keys, key=extract_date)