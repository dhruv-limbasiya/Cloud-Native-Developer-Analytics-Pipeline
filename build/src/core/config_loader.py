import yaml
from pathlib import Path


class ConfigLoader:
    """
    Load configuration from config/config.yaml
    """

    def __init__(self):
        self.config = None

    def load_config(self):
        config_path = Path("config/config.yaml")

        if not config_path.exists():
            raise FileNotFoundError(
                f"Configuration file not found: {config_path}"
            )

        with open(config_path, "r") as file:
            self.config = yaml.safe_load(file)

        return self.config

    def get_config(self):
        if self.config is None:
            return self.load_config()

        return self.config