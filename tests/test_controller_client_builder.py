import pytest
import pandas as pd
import requests

from api_to_dataframe import ClientBuilder


@pytest.fixture()
def setup():
    new_client = ClientBuilder(endpoint="https://economia.awesomeapi.com.br/last/USD-BRL")
    return new_client


@pytest.fixture()
def response_setup():
    new_client = ClientBuilder(endpoint="https://economia.awesomeapi.com.br/last/USD-BRL")
    return new_client.get_api_data()


def test_constructor_raises():
    with pytest.raises(ValueError):
        new_client = ClientBuilder(endpoint="")

    with pytest.raises(ValueError):
        new_client = ClientBuilder(
            endpoint="https://economia.awesomeapi.com.br/last/USD-BRL",
            retries=-1
        )

    with pytest.raises(ValueError):
        new_client = ClientBuilder(
            endpoint="https://economia.awesomeapi.com.br/last/USD-BRL",
            initial_delay=-1
        )

    with pytest.raises(ValueError):
        new_client = ClientBuilder(
            endpoint="https://economia.awesomeapi.com.br/last/USD-BRL",
            connection_timeout=-1
        )

    with pytest.raises(ValueError):
        new_client = ClientBuilder(
            endpoint="https://economia.awesomeapi.com.br/last/USD-BRL",
            retries=""
        )

    with pytest.raises(ValueError):
        new_client = ClientBuilder(
            endpoint="https://economia.awesomeapi.com.br/last/USD-BRL",
            initial_delay=""
        )

    with pytest.raises(ValueError):
        new_client = ClientBuilder(
            endpoint="https://economia.awesomeapi.com.br/last/USD-BRL",
            connection_timeout=""
        )


def test_constructor_with_param(setup):
    expected_result = "https://economia.awesomeapi.com.br/last/USD-BRL"
    new_client = setup
    assert new_client.endpoint == expected_result


def test_response_to_json(setup):
    new_client = setup
    response = new_client._get_raw_api_data()
    assert isinstance(response, requests.Response)


def test_to_dataframe(response_setup):
    df = ClientBuilder.api_to_dataframe(response_setup)
    assert isinstance(df, pd.DataFrame)