from src.extract.repositories import RepositoriesExtractor
from src.extract.commits import CommitsExtractor
from src.extract.contributors import ContributorsExtractor
from src.extract.issues import IssuesExtractor
from src.extract.pull_requests import PullRequestsExtractor
from src.extract.languages import LanguagesExtractor


class ExtractorFactory:

    @staticmethod
    def get_extractors(client):

        return {
            "repositories": RepositoriesExtractor(client),
            "commits": CommitsExtractor(client),
            "contributors": ContributorsExtractor(client),
            "issues": IssuesExtractor(client),
            "pull_requests": PullRequestsExtractor(client),
            "languages": LanguagesExtractor(client)
        }