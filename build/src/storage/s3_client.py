import io
import json

import boto3


class S3Client:
    """
    Amazon S3 helper class for reading and writing
    JSON and Parquet files.
    """

    def __init__(self):

        self.bucket_name = "developer-analytics-data"
        self.client = boto3.client("s3")
    
    # JSON

    def upload_json(self, key, data):

        self.client.put_object(
            Bucket=self.bucket_name,
            Key=key,
            Body=data,
            ContentType="application/json"
        )

        return f"s3://{self.bucket_name}/{key}"

    def download_json(self, key):

        response = self.client.get_object(
            Bucket=self.bucket_name,
            Key=key
        )

        return json.loads(
            response["Body"].read().decode("utf-8")
        )
    
    # Parquet

    def upload_parquet(self, dataframe, key):

        buffer = io.BytesIO()

        dataframe.to_parquet(
            buffer,
            engine="pyarrow",
            index=False
        )

        buffer.seek(0)

        self.client.put_object(
            Bucket=self.bucket_name,
            Key=key,
            Body=buffer.getvalue(),
            ContentType="application/octet-stream"
        )

        return f"s3://{self.bucket_name}/{key}"

    def download_parquet(self, key):

        import pandas as pd

        response = self.client.get_object(
            Bucket=self.bucket_name,
            Key=key
        )

        buffer = io.BytesIO(
            response["Body"].read()
        )

        return pd.read_parquet(buffer)
    
    # Utility

    def list_objects(self, prefix):

        keys = []

        paginator = self.client.get_paginator("list_objects_v2")

        pages = paginator.paginate(
            Bucket=self.bucket_name,
            Prefix=prefix
        )

        for page in pages:

            if "Contents" not in page:
                continue

            for obj in page["Contents"]:
                keys.append(obj["Key"])

        return keys