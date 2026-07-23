from src.core.config_loader import ConfigLoader
from src.core.logger import Logger

from src.pipeline.bronze.bronze_pipeline import BronzePipeline
from src.pipeline.silver.silver_pipeline import SilverPipeline
from src.pipeline.gold.gold_pipeline import GoldPipeline


def main():

    logger = Logger.get_logger()

    config = ConfigLoader().get_config()

    organization = config["github"]["organizations"][0]

    organization_endpoints = config["github"]["organization_endpoints"]

    repository_endpoints = config["github"]["repository_endpoints"]

    logger.info("=" * 60)
    logger.info("Starting Bronze Pipeline")
    logger.info("=" * 60)

    BronzePipeline().run(
        organization,
        organization_endpoints,
        repository_endpoints,
    )

    logger.info("=" * 60)
    logger.info("Starting Silver Pipeline")
    logger.info("=" * 60)

    SilverPipeline().run(
        organization,
        [
            "repositories",
            "languages",
            "contributors",
            "commits",
            "issues",
            "pull_requests",
        ],
    )

    logger.info("=" * 60)
    logger.info("Starting Gold Pipeline")
    logger.info("=" * 60)

    GoldPipeline().run(organization)

    logger.info("=" * 60)
    logger.info("Pipeline Completed Successfully")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()