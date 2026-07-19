from src.extract.github_client import GitHubClient
from src.extract.extractor_factory import ExtractorFactory

from src.storage.bronze_writer import BronzeWriter
from src.storage.metadata_writer import MetadataWriter

from src.pipeline.repository_pipeline import RepositoryPipeline


class BronzePipeline:

    def __init__(self):

        self.client = GitHubClient()

        self.writer = BronzeWriter()

        self.metadata = MetadataWriter()

        self.repository_pipeline = RepositoryPipeline(
            client=self.client,
            writer=self.writer,
            metadata=self.metadata,
            extractors=self.extractors
        )

        self.extractors = ExtractorFactory.get_extractors(self.client)

    def run(self, organization, organization_endpoints, repository_endpoints):

        for endpoint in organization_endpoints:

            print(f"\nProcessing {endpoint}")

            # Only organization-level endpoints are handled here.
            # Repository-level endpoints are processed inside RepositoryPipeline.
            if endpoint != "repositories":

                print(f"Skipping {endpoint} (Repository-level endpoint)")
                continue

            extractor = self.extractors.get(endpoint)

            if extractor is None:

                print(f"No extractor found for '{endpoint}'")
                continue

            try:
                
                # Extract
                data = extractor.extract(organization)
                
                # Save Bronze
                file_path = self.writer.save(
                    organization=organization,
                    endpoint=endpoint,
                    filename="repositories.json",
                    data=data
                )

                print(f"Saved -> {file_path}")
                
                # Save Metadata
                self.metadata.save(
                    organization=organization,
                    endpoint=endpoint,
                    record_count=len(data),
                    file_path=file_path,
                    status="SUCCESS"
                )

                # Start Repository Pipeline
                self.repository_pipeline.run(
                    organization=organization,
                    repositories=data,
                    endpoints=repository_endpoints
                )

            except Exception as e:

                print(f"Failed to process {endpoint}: {e}")

                self.metadata.save(
                    organization=organization,
                    endpoint=endpoint,
                    record_count=0,
                    file_path="",
                    status="FAILED"
                )