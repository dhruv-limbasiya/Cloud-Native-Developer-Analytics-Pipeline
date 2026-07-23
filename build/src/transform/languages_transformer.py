from src.transform.base_transformer import BaseTransformer


class LanguagesTransformer(BaseTransformer):

    def transform(
        self,
        repository_name,
        data
    ):

        records = []

        for language, bytes_of_code in data.items():

            records.append(
                {
                    "repository_name": repository_name,
                    "language": language,
                    "bytes_of_code": bytes_of_code
                }
            )

        return self.to_dataframe(records)