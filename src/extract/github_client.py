import time
import requests

from src.core.config_loader import ConfigLoader
from src.core.constants import BASE_URL
from src.core.env_loader import EnvLoader
from src.core.logger import Logger
from src.core.exceptions import GitHubAPIError


class GitHubClient:
    """
    Handles communication with GitHub REST API.
    """

    def __init__(self):

        self.logger = Logger.get_logger()

        self.config = ConfigLoader().get_config()

        token = EnvLoader().get_github_token()

        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json"
        }

    def get(self, endpoint, params=None):
        """
        Send GET request to GitHub API.
        """

        url = BASE_URL + endpoint

        retries = self.config["github"]["retry_count"]

        for attempt in range(retries):

            try:

                self.logger.info(f"GET {url}")

                response = requests.get(
                    url,
                    headers=self.headers,
                    params=params,
                    timeout=30
                )

                remaining = response.headers.get(
                    "X-RateLimit-Remaining"
                )

                self.logger.info(
                    f"Remaining Requests: {remaining}"
                )

                if response.status_code == 200:
                    return response.json()

                if response.status_code >= 500:

                    self.logger.warning(
                        f"Retry {attempt + 1}"
                    )

                    time.sleep(2)

                    continue

                raise GitHubAPIError(
                    f"GitHub API Error: {response.status_code}"
                )

            except requests.exceptions.RequestException:

                self.logger.warning(
                    f"Retry {attempt + 1}"
                )

                time.sleep(2)

        raise GitHubAPIError(
            "Maximum retry attempts reached."
        )

    def paginate(self, endpoint):
        """
        Automatically fetch all pages.
        """

        page = 1

        all_data = []

        per_page = self.config["github"]["per_page"]

        while True:

            self.logger.info(f"Fetching Page {page}")

            data = self.get(
                endpoint,
                params={
                    "per_page": per_page,
                    "page": page
                }
            )

            if len(data) == 0:
                break

            all_data.extend(data)

            page += 1

        return all_data