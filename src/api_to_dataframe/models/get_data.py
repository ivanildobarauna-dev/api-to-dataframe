import requests
import pandas as pd


class GetData:
    @staticmethod
    def get_response(endpoint: str, headers: dict, connection_timeout: int):
        response = requests.get(endpoint, timeout=connection_timeout, headers=headers)
        response.raise_for_status()
        return response

    @staticmethod
    def to_dataframe(response):
        try:
            df = pd.DataFrame(response)
        except Exception as err:
            raise TypeError(
                f"Invalid response for transform in dataframe: {err}"
            ) from err

        if df.empty:
            raise ValueError("::: DataFrame is empty :::")

        return df
