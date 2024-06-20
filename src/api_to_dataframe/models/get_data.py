import requests
from requests.exceptions import HTTPError, Timeout
import pandas as pd

# from api_to_dataframe.common.utils.retry_strategies import RetryStrategies
from api_to_dataframe.models.retainer import RetryStrategies


class GetData:
    @staticmethod
    def get_response(endpoint: str,
                     headers: dict,
                     connection_timeout: int):



        response = requests.get(endpoint, timeout=connection_timeout, headers=headers)
        response.raise_for_status()
        return response
    @staticmethod
    def to_dataframe(response):
        try:
            df = pd.DataFrame(response)
        except Exception as err:
            raise TypeError(f"Invalid response for transform in dataframe: {err}")

        if df.empty:
            raise ValueError("::: DataFrame is empty :::")
        else:
            return df
