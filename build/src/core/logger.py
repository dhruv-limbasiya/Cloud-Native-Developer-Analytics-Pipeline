import logging
import os
from pathlib import Path


class Logger:

    @staticmethod
    def get_logger():

        logger = logging.getLogger("github_pipeline")

        if logger.handlers:
            return logger

        logger.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        )

        # Running inside AWS Lambda?
        is_lambda = "AWS_LAMBDA_FUNCTION_NAME" in os.environ

        if not is_lambda:
            log_folder = Path("logs")
            log_folder.mkdir(exist_ok=True)

            file_handler = logging.FileHandler("logs/pipeline.log")
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        return logger