from api_to_dataframe.models.retainer import retry_strategies, Strategies
from api_to_dataframe.models.get_data import GetData
from api_to_dataframe.utils.logger import logger, telemetry
import time


class ClientBuilder:
    def __init__(  # pylint: disable=too-many-positional-arguments,too-many-arguments
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
            retry_strategy (Strategies, optional): Defaults to Strategies.NO_RETRY_STRATEGY.
            retries (int): The number of times to retry a failed request. Defaults to 3.
            initial_delay (int): The delay between retries in seconds. Defaults to 1.
            connection_timeout (int): The timeout for the connection in seconds. Defaults to 1.

        Raises:
            ValueError: If endpoint is an empty string.
            ValueError: If retries is not a non-negative integer.
            ValueError: If delay is not a non-negative integer.
            ValueError: If connection_timeout is not a non-negative integer.
        """

        if headers is None:
            headers = {}
        if endpoint == "":
            error_msg = "endpoint cannot be an empty string"
            logger.error(error_msg)
            telemetry.logs().new_log(
                msg=error_msg,
                tags={"component": "ClientBuilder", "method": "__init__"},
                level=40  # ERROR level
            )
            raise ValueError
        if not isinstance(retries, int) or retries < 0:
            error_msg = "retries must be a non-negative integer"
            logger.error(error_msg)
            telemetry.logs().new_log(
                msg=error_msg,
                tags={"component": "ClientBuilder", "method": "__init__"},
                level=40  # ERROR level
            )
            raise ValueError
        if not isinstance(initial_delay, int) or initial_delay < 0:
            error_msg = "initial_delay must be a non-negative integer"
            logger.error(error_msg)
            telemetry.logs().new_log(
                msg=error_msg,
                tags={"component": "ClientBuilder", "method": "__init__"},
                level=40  # ERROR level
            )
            raise ValueError
        if not isinstance(connection_timeout, int) or connection_timeout < 0:
            error_msg = "connection_timeout must be a non-negative integer"
            logger.error(error_msg)
            telemetry.logs().new_log(
                msg=error_msg,
                tags={"component": "ClientBuilder", "method": "__init__"},
                level=40  # ERROR level
            )
            raise ValueError

        self.endpoint = endpoint
        self.retry_strategy = retry_strategy
        self.connection_timeout = connection_timeout
        self.headers = headers
        self.retries = retries
        self.delay = initial_delay

        # Record client initialization metric
        telemetry.metrics().metric_increment(
            name="client.initialization",
            tags={
                "endpoint": endpoint,
                "retry_strategy": retry_strategy.name,
                "connection_timeout": str(connection_timeout)
            }
        )

        # Log initialization
        telemetry.logs().new_log(
            msg=f"ClientBuilder initialized with endpoint {endpoint}",
            tags={
                "endpoint": endpoint,
                "retry_strategy": retry_strategy.name,
                "connection_timeout": str(connection_timeout),
                "component": "ClientBuilder"
            },
            level=20  # INFO level
        )

    @retry_strategies
    def get_api_data(self):
        """
        Retrieves data from the API using the defined endpoint and retry strategy.

        This function sends a request to the API using the endpoint, headers, and
        connection timeout specified in the instance attributes. It uses the
        defined retry strategy to handle potential failures and retries.

        Returns:
            dict: The JSON response from the API as a dictionary.
        """
        # Use the telemetry spans with new API
        span = telemetry.traces().new_span("get_api_data")
        try:
            # Add span attributes
            span.set_attribute("endpoint", self.endpoint)
            span.set_attribute("retry_strategy", self.retry_strategy.name)
            span.set_attribute("connection_timeout", self.connection_timeout)

            # Log the API request
            telemetry.logs().new_log(
                msg=f"Making API request to {self.endpoint}",
                tags={
                    "endpoint": self.endpoint,
                    "component": "ClientBuilder",
                    "method": "get_api_data"
                },
                level=20  # INFO level
            )

            # Record the start time for response time measurement
            start_time = time.time()

            # Make the API request
            response = GetData.get_response(
                endpoint=self.endpoint,
                headers=self.headers,
                connection_timeout=self.connection_timeout,
            )

            # Calculate response time
            response_time = time.time() - start_time

            # Record response time as histogram
            telemetry.metrics().record_histogram(
                name="api.response_time",
                tags={"endpoint": self.endpoint},
                value=response_time
            )

            # Record successful request metric
            telemetry.metrics().metric_increment(
                name="api.request.success",
                tags={"endpoint": self.endpoint}
            )

            # Log success
            telemetry.logs().new_log(
                msg=f"API request to {self.endpoint} successful",
                tags={
                    "endpoint": self.endpoint,
                    "response_status": response.status_code,
                    "response_time": response_time,
                    "component": "ClientBuilder",
                    "method": "get_api_data"
                },
                level=20  # INFO level
            )

            return response.json()
        finally:
            span.end()

    @staticmethod
    def api_to_dataframe(response: dict):
        """
        Converts an API response to a DataFrame.

        This function takes a dictionary response from an API,
        uses the `to_dataframe` function from the `GetData` class
        to convert it into a DataFrame, and logs the operation as successful.

        Args:
            response (dict): The dictionary containing the API response.

        Returns:
            DataFrame: A pandas DataFrame containing the data from the API response.
        """
        # Use telemetry with new API
        span = telemetry.traces().new_span("api_to_dataframe")
        try:
            response_size = len(response) if isinstance(response, list) else 1
            span.set_attribute("response_size", response_size)

            # Log conversion start
            telemetry.logs().new_log(
                msg="Converting API response to DataFrame",
                tags={
                    "response_size": response_size,
                    "response_type": type(response).__name__,
                    "component": "ClientBuilder",
                    "method": "api_to_dataframe"
                },
                level=20  # INFO level
            )

            try:
                # Convert to dataframe
                df = GetData.to_dataframe(response)

                # Record metrics
                telemetry.metrics().metric_increment(
                    name="dataframe.conversion.success",
                    tags={"size": len(df)}
                )

                # Log success
                telemetry.logs().new_log(
                    msg="Successfully converted API response to DataFrame",
                    tags={
                        "dataframe_rows": len(df),
                        "dataframe_columns": len(df.columns),
                        "component": "ClientBuilder",
                        "method": "api_to_dataframe"
                    },
                    level=20  # INFO level
                )

                return df

            except Exception as e:
                # Record failure metric
                telemetry.metrics().metric_increment(
                    name="dataframe.conversion.failure",
                    tags={"error_type": type(e).__name__}
                )

                # Log error
                error_msg = f"Failed to convert API response to DataFrame: {str(e)}"
                telemetry.logs().new_log(
                    msg=error_msg,
                    tags={
                        "error": str(e),
                        "error_type": type(e).__name__,
                        "component": "ClientBuilder",
                        "method": "api_to_dataframe"
                    },
                    level=40  # ERROR level
                )

                # Re-raise the exception
                raise
        finally:
            span.end()
