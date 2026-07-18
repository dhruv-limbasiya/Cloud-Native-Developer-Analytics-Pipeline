from src.extract.github_client import GitHubClient


class PullRequestsExtractor:

    def __init__(self, client: GitHubClient):
        self.client = client

    def extract(self, owner, repository):

        endpoint = f"/repos/{owner}/{repository}/pulls"

        return self.client.paginate(endpoint)