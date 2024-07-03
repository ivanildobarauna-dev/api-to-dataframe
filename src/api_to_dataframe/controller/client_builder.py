from api_to_dataframe.models.retainer import retry_strategies, Strategies
from api_to_dataframe.models.get_data import GetData
from api_to_dataframe.utils.logger import log, LogLevel


class ClientBuilder:
    def __init__(  # pylint: disable=too-many-arguments
        self,
        endpoint: str,
        headers: dict = None,
        retry_strategy: Strategies = Strategies.NO_RETRY_STRATEGY,
        retries: int = 3,
        initial_delay: int = 1,
        connection_timeout: int = 1,
    ):
        """
        Initializes the ClientBuilder object.

        Args:
            endpoint (str): The API endpoint to connect to.
            headers (dict, optional): The headers to use for the API request. Defaults to None.
            retry_strategy (Strategies, optional): Defaults to Strategies.NoRetryStrategy.
            retries (int): The number of times to retry a failed request. Defaults to 3.
            initial_delay (int): The delay between retries in seconds. Defaults to 1.
            connection_timeout (int): The timeout for the connection in seconds. Defaults to 2.

        Raises:
            ValueError: If endpoint is an empty string.
            ValueError: If retries is not a non-negative integer.
            ValueError: If delay is not a non-negative integer.
            ValueError: If connection_timeout is not a non-negative integer.
        """

        if headers is None:
            headers = {}
        if endpoint == "":
            log("endpoint param is mandatory", LogLevel.ERROR)
            raise ValueError
        if not isinstance(retries, int) or retries < 0:
            log("retries must be a non-negative integer", LogLevel.ERROR)
            raise ValueError
        if not isinstance(initial_delay, int) or initial_delay < 0:
            log("delay must be a non-negative integer", LogLevel.ERROR)
            raise ValueError
        if not isinstance(connection_timeout, int) or connection_timeout < 0:
            log("connection_timeout must be a non-negative integer", LogLevel.ERROR)
            raise ValueError

        self.endpoint = endpoint
        self.retry_strategy = retry_strategy
        self.connection_timeout = connection_timeout
        self.headers = headers
        self.retries = retries
        self.delay = initial_delay

    @retry_strategies
    def get_api_data(self):
        """
        Retrieves data from the API using the defined endpoint and retry strategy.

        Returns:
            dict: The response from the API.
        """
        response = GetData.get_response(
            endpoint=self.endpoint,
            headers=self.headers,
            connection_timeout=self.connection_timeout,
        )

        return response.json()

    def _get_raw_api_data(self):
        response = GetData.get_response(
            endpoint=self.endpoint,
            headers=self.headers,
            connection_timeout=self.connection_timeout,
        )
        return response

    @staticmethod
    def api_to_dataframe(response: dict):
        df = GetData.to_dataframe(response)
        log("serialized to dataframe: OK", LogLevel.INFO)
        return df
