from src.transform.repositories_transformer import RepositoriesTransformer
from src.transform.languages_transformer import LanguagesTransformer
from src.transform.contributors_transformer import ContributorsTransformer
from src.transform.commits_transformer import CommitsTransformer
from src.transform.issues_transformer import IssuesTransformer
from src.transform.pull_requests_transformer import PullRequestsTransformer

class TransformerFactory:

    @staticmethod
    def get_transformers():

        return {

            "repositories": RepositoriesTransformer(),

            "languages": LanguagesTransformer(),
            "contributors": ContributorsTransformer(),
            "commits": CommitsTransformer(),
            "issues": IssuesTransformer(),
            "pull_requests": PullRequestsTransformer(),
        }