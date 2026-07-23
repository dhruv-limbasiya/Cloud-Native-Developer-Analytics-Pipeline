from pathlib import Path


class FileManager:

    @staticmethod
    def create_directory(path: Path):
        """
        Create directory if it does not exist.
        """
        path.mkdir(parents=True, exist_ok=True)