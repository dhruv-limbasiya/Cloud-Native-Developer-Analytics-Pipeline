from src.extract.github_client import GitHubClient
from src.extract.extractor_factory import ExtractorFactory
from src.storage.bronze_writer import BronzeWriter
from src.storage.metadata_writer import MetadataWriter


class BronzePipeline:

    def __init__(self):

        self.client = GitHubClient()
        self.writer = BronzeWriter()
        self.metadata = MetadataWriter()

        self.extractors = ExtractorFactory.get_extractors(self.client)

    def run(self, organization, endpoints):

        for endpoint in endpoints:

            print(f"\nProcessing {endpoint}")

            # Skip repository-level endpoints for now
            if endpoint != "repositories":
                print(f"Skipping {endpoint} (Repository-level endpoint)")
                continue

            extractor = self.extractors.get(endpoint)

            if extractor is None:
                print(f"No extractor found for '{endpoint}'")
                continue

            try:

                # Extract raw data
                data = extractor.extract(organization)

                # Save Bronze
                file_path = self.writer.save(
                    organization=organization,
                    endpoint=endpoint,
                    filename=f"{endpoint}.json",
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

            except Exception as e:

                print(f"Failed to process {endpoint}: {e}")

                self.metadata.save(
                    organization=organization,
                    endpoint=endpoint,
                    record_count=0,
                    file_path="",
                    status="FAILED"
                )