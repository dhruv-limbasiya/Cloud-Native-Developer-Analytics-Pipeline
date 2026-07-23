import json
from datetime import datetime

from src.storage.s3_client import S3Client


class BronzeWriter:

    def __init__(self):
        self.s3 = S3Client()

    def save(
        self,
        organization,
        endpoint,
        filename,
        data
    ):

        today = datetime.now()

        key = (
            f"bronze/"
            f"organization={organization}/"
            f"endpoint={endpoint}/"
            f"year={today.year}/"
            f"month={today.month:02d}/"
            f"day={today.day:02d}/"
            f"{filename}"
        )

        json_data = json.dumps(data, indent=4)

        s3_path = self.s3.upload_json(
            key,
            json_data
        )

        return s3_path