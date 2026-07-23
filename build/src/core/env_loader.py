import os

from dotenv import load_dotenv


class EnvLoader:

    def __init__(self):
        load_dotenv()

    def get_github_token(self):

        token = os.getenv("GITHUB_TOKEN")

        if token is None:
            raise ValueError(
                "GITHUB_TOKEN not found in .env file."
            )

        return token

    def get_aws_region(self):

        return os.getenv("AWS_REGION")