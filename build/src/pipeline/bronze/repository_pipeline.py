class RepositoryPipeline:

    def __init__(
        self,
        client,
        writer,
        metadata,
        extractors
    ):

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

        print("\nStarting Repository Pipeline")
        max_repositories = self.client.config["github"]["max_repositories"]

        # Development mode
        for repository in repositories[:max_repositories]:

            repo_name = repository["name"]

            print(f"\nRepository : {repo_name}")

            for endpoint in endpoints:

                extractor = self.extractors.get(endpoint)

                if extractor is None:

                    print(f"{endpoint} extractor not implemented")

                    continue

                try:

                    print(f"Fetching {endpoint}")

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

                    print(f"Saved -> {file_path}")

                    self.metadata.save(
                        organization=organization,
                        endpoint=endpoint,
                        record_count=len(data),
                        file_path=file_path,
                        status="SUCCESS"
                    )

                except Exception as e:

                    print(f"{endpoint} failed : {e}")

                    self.metadata.save(
                        organization=organization,
                        endpoint=endpoint,
                        record_count=0,
                        file_path="",
                        status="FAILED"
                    )