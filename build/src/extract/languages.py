class LanguagesExtractor:

    def __init__(self, client):
        self.client = client

    def extract(self, owner, repository):

        endpoint = f"/repos/{owner}/{repository}/languages"

        return self.client.get(endpoint)