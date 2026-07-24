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

        # Repository endpoint
        if "endpoint=repositories" not in prefix:

            latest_date = max(
                self._extract_date(key)
                for key in keys
            )

            latest_keys = [
                key
                for key in keys
                if self._extract_date(key) == latest_date
            ]

            bronze_files = []

            for key in sorted(latest_keys):

                self.logger.info(f"Reading Bronze file: {key}")
                partition = self._extract_partition(key)

                bronze_files.append(
                    {
                        "file_name": key.split("/")[-1],
                        "data": self.s3.download_json(key),

                        "year": partition["year"],
                        "month": partition["month"],
                        "day": partition["day"]
                    }
                )

            return bronze_files

        # repositories.json
        latest_key = self._get_latest_key(keys)

        self.logger.info(
            f"Reading latest Bronze snapshot: {latest_key}"
        )

        partition = self._extract_partition(latest_key)

        return [
            {
                "file_name": latest_key.split("/")[-1],
                "data": self.s3.download_json(latest_key),

                "year": partition["year"],
                "month": partition["month"],
                "day": partition["day"]
            }
        ]
    
    def _extract_date(self, key):

        parts = key.split("/")

        year = month = day = None

        for part in parts:

            if part.startswith("year="):
                year = int(part.split("=")[1])

            elif part.startswith("month="):
                month = int(part.split("=")[1])

            elif part.startswith("day="):
                day = int(part.split("=")[1])

        return datetime(year, month, day)    

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
    
    
    def _extract_partition(self, key):

        parts = key.split("/")

        partition = {}

        for part in parts:

            if part.startswith("year="):
                partition["year"] = part.split("=")[1]

            elif part.startswith("month="):
                partition["month"] = part.split("=")[1]

            elif part.startswith("day="):
                partition["day"] = part.split("=")[1]

        return partition