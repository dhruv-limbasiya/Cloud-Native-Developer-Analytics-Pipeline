import logging
from pathlib import Path


class Logger:

    @staticmethod
    def get_logger():

        log_folder = Path("logs")
        log_folder.mkdir(exist_ok=True)

        logger = logging.getLogger("github_pipeline")

        if logger.handlers:
            return logger

        logger.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        )

        file_handler = logging.FileHandler(
            "logs/pipeline.log"
        )

        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()

        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger