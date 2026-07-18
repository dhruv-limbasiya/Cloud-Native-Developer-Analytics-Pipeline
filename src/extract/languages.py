from src.extract.github_client import GitHubClient


class LanguagesExtractor:

    def __init__(self, client: GitHubClient):
        self.client = client

    def extract(self, owner, repository):

        endpoint = f"/repos/{owner}/{repository}/languages"

        return self.client.get(endpoint)