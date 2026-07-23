import pandas as pd


class BaseTransformer:
    """
    Base class for all Silver transformers.
    """

    def __init__(self):
        pass

    def to_dataframe(self, data):
        """
        Convert list of dictionaries to DataFrame.
        """

        return pd.DataFrame(data)

    def convert_datetime(
        self,
        dataframe,
        columns
    ):
        """
        Convert columns to datetime.
        """

        for column in columns:

            if column in dataframe.columns:

                dataframe[column] = pd.to_datetime(
                    dataframe[column],
                    errors="coerce",
                    utc=True
                )

        return dataframe

    def fill_nulls(
        self,
        dataframe,
        value=""
    ):
        """
        Replace missing values.
        """

        return dataframe.fillna(value)

    def rename_columns(
        self,
        dataframe,
        mapping
    ):
        """
        Rename columns.
        """

        return dataframe.rename(
            columns=mapping
        )

    def select_columns(
        self,
        dataframe,
        columns
    ):
        """
        Keep only required columns.
        """

        existing_columns = [
            column
            for column in columns
            if column in dataframe.columns
        ]

        return dataframe[existing_columns]

    def transform(self, repository_name , data):
        """
        Must be implemented by child classes.
        """

        raise NotImplementedError