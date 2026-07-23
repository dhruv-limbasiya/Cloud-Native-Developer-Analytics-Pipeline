from src.transform.base_transformer import BaseTransformer


class ContributorsTransformer(BaseTransformer):
    """
    Transform GitHub contributors response.
    """

    def transform(
        self,
        repository_name,
        data
    ):

        dataframe = self.to_dataframe(data)

        dataframe["repository_name"] = repository_name

        dataframe = self.select_columns(
            dataframe,
            [
                "repository_name",
                "login",
                "id",
                "node_id",
                "type",
                "site_admin",
                "contributions"
            ]
        )

        dataframe = self.rename_columns(
            dataframe,
            {
                "id": "contributor_id",
                "login": "contributor_login"
            }
        )

        dataframe = self.fill_nulls(dataframe)

        return dataframe