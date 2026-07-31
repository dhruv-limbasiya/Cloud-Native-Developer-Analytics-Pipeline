from src.core.logger import Logger


class RepositoryPipeline:

    def __init__(
        self,
        client,
        writer,
        metadata,
        extractors
    ):

        self.logger = Logger.get_logger()

        self.client = client
        self.writer = writer
        self.metadata = metadata
        self.extractors = extractors

    def run(
        self,
        organization,
        repositories,
        endpoints
    ):

        self.logger.info("Starting Repository Pipeline")
        max_repositories = self.client.config["github"]["max_repositories"]

        # Development mode
        for repository in repositories[:max_repositories]:

            repo_name = repository["name"]

            self.logger.info(f"Repository : {repo_name}")

            for endpoint in endpoints:

                extractor = self.extractors.get(endpoint)

                if extractor is None:

                    self.logger.warning(f"{endpoint} extractor not implemented")

                    continue

                try:

                    self.logger.info(f"Fetching {endpoint}")

                    data = extractor.extract(
                        organization,
                        repo_name
                    )

                    file_path = self.writer.save(
                        organization=organization,
                        endpoint=endpoint,
                        filename=f"{repo_name}.json",
                        data=data
                    )

                    self.logger.info(f"Saved -> {file_path}")

                    self.metadata.save(
                        organization=organization,
                        endpoint=endpoint,
                        record_count=len(data),
                        file_path=file_path,
                        status="SUCCESS"
                    )

                except Exception as e:

                    self.logger.error(f"{endpoint} failed : {e}")

                    self.metadata.save(
                        organization=organization,
                        endpoint=endpoint,
                        record_count=0,
                        file_path="",
                        status="FAILED"
                    )