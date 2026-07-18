import json
from datetime import datetime
from pathlib import Path

from src.storage.file_manager import FileManager


class BronzeWriter:

    def save(
        self,
        organization,
        endpoint,
        filename,
        data
    ):

        today = datetime.now()

        folder = (
            Path("data")
            / "bronze"
            / f"organization={organization}"
            / f"endpoint={endpoint}"
            / f"year={today.year}"
            / f"month={today.month:02d}"
            / f"day={today.day:02d}"
        )

        FileManager.create_directory(folder)

        file_path = folder / filename

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        return file_path