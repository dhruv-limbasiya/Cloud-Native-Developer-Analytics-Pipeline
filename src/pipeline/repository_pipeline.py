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

    def run(self, organization, repositories,endpoints):

        print("\nStarting Repository Pipeline")

        for repository in repositories[:5]:

            repo_name = repository["name"]

            print(f"\nRepository : {repo_name}")
            
            for endpoint in endpoints:
                extractor = self.extractors.get(endpoint)

                if extractor is None:
                    continue

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

                self.metadata.save(
                    organization=organization,
                    endpoint=endpoint,
                    record_count=len(data),
                    file_path=file_path,
                    status="SUCCESS"
                )