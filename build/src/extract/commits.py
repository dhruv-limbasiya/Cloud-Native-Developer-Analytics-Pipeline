from src.extract.github_client import GitHubClient


class CommitsExtractor:

    def __init__(self, client: GitHubClient):
        self.client = client

    def extract(self, owner, repository):

        endpoint = f"/repos/{owner}/{repository}/commits"

        return self.client.paginate(endpoint)