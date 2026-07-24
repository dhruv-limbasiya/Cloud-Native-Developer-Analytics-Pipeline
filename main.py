from src.core.config_loader import ConfigLoader
from src.core.logger import Logger

from src.pipeline.silver.silver_pipeline import SilverPipeline
from src.pipeline.gold.gold_pipeline import GoldPipeline

from src.serving.postgres_loader import PostgresLoader


def main():

    logger = Logger.get_logger()

    config = ConfigLoader().get_config()

    organization = config["github"]["organizations"][0]

    logger.info("=" * 60)
    logger.info("Starting Local Analytics Pipeline")
    logger.info("=" * 60)

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
    logger.info("Loading Data into PostgreSQL")
    logger.info("=" * 60)

    PostgresLoader().run(organization)

    logger.info("=" * 60)
    logger.info("Pipeline Completed Successfully")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()