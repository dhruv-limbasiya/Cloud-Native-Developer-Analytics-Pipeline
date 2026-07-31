from src.core.logger import Logger
from src.extract.github_client import GitHubClient
from src.extract.extractor_factory import ExtractorFactory

from src.storage.bronze_writer import BronzeWriter
from src.storage.metadata_writer import MetadataWriter

from src.pipeline.bronze.repository_pipeline import RepositoryPipeline


class BronzePipeline:

    def __init__(self):

        self.logger = Logger.get_logger()

        self.client = GitHubClient()

        self.writer = BronzeWriter()

        self.metadata = MetadataWriter()
        
        self.extractors = ExtractorFactory.get_extractors(self.client)

        self.repository_pipeline = RepositoryPipeline(
            client=self.client,
            writer=self.writer,
            metadata=self.metadata,
            extractors=self.extractors
        )

    def run(self, organization, organization_endpoints, repository_endpoints):

        for endpoint in organization_endpoints:

            self.logger.info(f"Processing {endpoint}")
            
            if endpoint != "repositories":

                self.logger.info(f"Skipping {endpoint} (Repository-level endpoint)")
                continue

            extractor = self.extractors.get(endpoint)

            if extractor is None:

                self.logger.warning(f"No extractor found for '{endpoint}'")
                continue

            try:
                
                # Extract
                data = extractor.extract(organization)

                max_repositories = self.client.config["github"]["max_repositories"]

                data = data[:max_repositories]
                
                # Save Bronze
                file_path = self.writer.save(
                    organization=organization,
                    endpoint=endpoint,
                    filename="repositories.json",
                    data=data
                )

                self.logger.info(f"Saved -> {file_path}")
                
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

                self.logger.error(f"Failed to process {endpoint}: {e}")

                self.metadata.save(
                    organization=organization,
                    endpoint=endpoint,
                    record_count=0,
                    file_path="",
                    status="FAILED"
                )