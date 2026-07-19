from src.core.config_loader import ConfigLoader
from src.core.logger import Logger
from src.pipeline.bronze_pipeline import BronzePipeline


def main():

    logger = Logger.get_logger()

    logger.info("Starting Bronze Pipeline")

    config = ConfigLoader().get_config()

    organization = config["github"]["organizations"][0]

    organization_endpoints = config["github"]["organization_endpoints"]

    repository_endpoints = config["github"]["repository_endpoints"]

    pipeline = BronzePipeline()

    pipeline.run(
        organization,
        organization_endpoints,
        repository_endpoints
    )


if __name__ == "__main__":
    main()