import json
from pathlib import Path
from datetime import datetime


class MetadataWriter:

    def save(
        self,
        organization,
        endpoint,
        record_count,
        file_path,
        status
    ):

        metadata = {
            "run_time": datetime.now().isoformat(),

            "organization": organization,

            "endpoint": endpoint,

            "record_count": record_count,

            "status": status,

            "file_path": str(file_path)
        }

        metadata_folder = Path("data") / "metadata"

        metadata_folder.mkdir(
            parents=True,
            exist_ok=True
        )

        metadata_file = metadata_folder / "pipeline_runs.json"

        if metadata_file.exists():

            with open(metadata_file, "r") as file:

                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    data = []

        else:
            data = []

        data.append(metadata)

        with open(metadata_file, "w") as file:

            json.dump(
                data,
                file,
                indent=4
            )