from src.extract.github_client import GitHubClient


class ContributorsExtractor:

    def __init__(self, client: GitHubClient):
        self.client = client

    def extract(self, owner, repository):

        endpoint = f"/repos/{owner}/{repository}/contributors"

        return self.client.paginate(endpoint)