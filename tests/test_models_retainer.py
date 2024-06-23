from api_to_dataframe import ClientBuilder, RetryStrategies
import requests
import time
import pytest


def test_linear_strategy():
    endpoint = "https://api-to-dataframe/"
    max_retries = 2
    client = ClientBuilder(
        endpoint=endpoint,
        retry_strategy=RetryStrategies.LinearRetryStrategy,
        retries=max_retries,
        initial_delay=1,
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


def test_no_retry_strategy():
    endpoint = "https://api-to-dataframe/"
    client = ClientBuilder(
        endpoint=endpoint,
        retry_strategy=RetryStrategies.NoRetryStrategy,
    )

    with pytest.raises(requests.exceptions.RequestException) as e:
        client.get_api_data()


def test_exponential_strategy():
    endpoint = "https://api-to-dataframe/"
    max_retries = 2
    client = ClientBuilder(
        endpoint=endpoint,
        retry_strategy=RetryStrategies.ExponentialRetryStrategy,
        retries=max_retries,
        initial_delay=1,
        connection_timeout=1
    )

    retry_number = 0

    while retry_number < max_retries:
        try:
            start = time.time()
            client.get_api_data()
        except requests.exceptions.RequestException as e:
            end = time.time()
            assert end - start >= client.delay * 2 ** retry_number
            retry_number += 1

    assert retry_number == max_retries
