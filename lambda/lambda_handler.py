import os
import sys
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from src.core.config_loader import ConfigLoader
from src.core.logger import Logger
from src.pipeline.bronze.bronze_pipeline import BronzePipeline


logger = Logger.get_logger()


def lambda_handler(event, context):
    """
    AWS Lambda Entry Point

    Executes only the Bronze pipeline.
    """

    try:

        logger.info("=" * 60)
        logger.info("AWS Lambda Started")
        logger.info("=" * 60)

        config = ConfigLoader().get_config()

        organization = config["github"]["organizations"][0]

        organization_endpoints = config["github"]["organization_endpoints"]

        repository_endpoints = config["github"]["repository_endpoints"]

        BronzePipeline().run(
            organization,
            organization_endpoints,
            repository_endpoints,
        )

        logger.info("=" * 60)
        logger.info("Bronze Pipeline Completed")
        logger.info("=" * 60)
        
        print("GitHub Actions deployment successful!")

        return {
            "statusCode": 200,
            "body": {
                "message": "Bronze pipeline executed successfully."
            },
        }

    except Exception as ex:

        logger.exception(ex)

        return {
            "statusCode": 500,
            "body": {
                "message": str(ex)
            },
        }