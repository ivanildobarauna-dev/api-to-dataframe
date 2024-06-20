from api_to_dataframe.models.retainer import RetryStrategies
from api_to_dataframe.models.retainer import Strategies
from api_to_dataframe.models.get_data import GetData


class ClientBuilder:
    def __init__(self,
                 endpoint: str,
                 headers: dict = {},
                 retry_strategy: Strategies = Strategies.NoRetryStrategy,
                 retries: int = 3,
                 delay: int = 1,
                 connection_timeout: int = 2):
        """
        Initializes an instance of ClientBuilder.

        Args:
            endpoint (str): The API endpoint to be accessed.
            retry_strategy (RetryStrategies, optional): The retry strategy for the request. Default is NoRetryStrategy.
            connection_timeout (int, optional): The timeout for the request. Default is 5 seconds.

        Raises:
            ValueError: If the endpoint is empty.
        """
        if endpoint == "":
            raise ValueError("::: endpoint param is mandatory :::")
        else:
            self.endpoint = endpoint
            self.retry_strategy = retry_strategy
            self.connection_timeout = connection_timeout
            self.headers = headers
            self.retries = retries
            self.delay = delay

    @RetryStrategies
    def get_api_data(self):
        """
        Retrieves data from the API using the defined endpoint and retry strategy.

        Returns:
            dict: The response from the API.
        """
        response = GetData.get_response(
            endpoint=self.endpoint,
            headers=self.headers,
            connection_timeout=self.connection_timeout
        )
        return response

    @staticmethod
    def api_to_dataframe(response: dict):
        """
        Converts the API response into a DataFrame.

        Args:
            response (dict): The response from the API.

        Returns:
            DataFrame: The data converted into a DataFrame.
        """
        df = GetData.to_dataframe(response)
        return df
