from src.extract.github_client import GitHubClient


class IssuesExtractor:

    def __init__(self, client: GitHubClient):
        self.client = client

    def extract(self, owner, repository):

        endpoint = f"/repos/{owner}/{repository}/issues"

        return self.client.paginate(endpoint)