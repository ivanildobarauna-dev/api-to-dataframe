import requests
from requests.exceptions import HTTPError, Timeout
import pandas as pd

# from api_to_dataframe.common.utils.retry_strategies import RetryStrategies
from api_to_dataframe.models.retainer import RetryStrategies


class GetData:
    @staticmethod
    def get_response(endpoint: str,
                     headers: dict,
                     retry_strategy: RetryStrategies,
                     timeout: int):

        try_number = 0

        response = requests.get(endpoint, timeout=timeout, headers=headers)

        if response.status_code == 200:
            return response
        else:
            try_number += 1
            # Retainer.strategy(retry_strategy)

    @staticmethod
    def to_dataframe(response):
        try:
            df = pd.DataFrame(response.json())
        except Exception as err:
            raise TypeError(f"Invalid response for transform in dataframe: {err}")

        if df.empty:
            raise ValueError("::: DataFrame is empty :::")
        else:
            return df
