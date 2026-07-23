from src.extract.github_client import GitHubClient


class RepositoriesExtractor:
    """
    Extract repositories from a GitHub organization.
    """

    def __init__(self, client: GitHubClient):
        self.client = client

    def extract(self, organization):

        endpoint = f"/orgs/{organization}/repos"

        return self.client.paginate(endpoint)