from api_to_dataframe import ClientBuilder, RetryStrategies
import requests
import time


def test_linear_strategy():
    endpoint = "https://api-to-dataframe/"
    max_retries = 2
    client = ClientBuilder(
        endpoint=endpoint,
        retry_strategy=RetryStrategies.LinearRetryStrategy,
        retries=max_retries,
        delay=1,
        connection_timeout=1
    )

    retry_number = 0

    while retry_number < max_retries:
        try:
            start = time.time()
            client.get_api_data()
        except requests.exceptions.RequestException as e:
            end = time.time()
            assert end - start >= client.delay
            retry_number += 1

    assert retry_number == max_retries
