from src.storage.s3_client import S3Client


class ParquetReader:

    def __init__(self):

        self.s3 = S3Client()

    def read_directory(self, prefix):

        keys = self.s3.list_objects(prefix)

        parquet_files = []

        for key in keys:

            if not key.endswith(".parquet"):
                continue

            dataframe = self.s3.download_parquet(key)

            parquet_files.append(
                {
                    "file_name": key.split("/")[-1],
                    "data": dataframe,
                    "key": key,
                }
            )

        return parquet_files