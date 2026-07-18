from src.models.repository import Repository


class RepositoryProcessor:

    def process(self, repositories):

        processed = []

        for repo in repositories:

            processed.append(
                Repository(repo)
            )

        return processed