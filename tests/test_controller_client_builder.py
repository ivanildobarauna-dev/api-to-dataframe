import pytest
import pandas as pd

from api_to_dataframe import ClientBuilder


@pytest.fixture()
def client_setup():
    new_client = ClientBuilder(
        endpoint="https://economia.awesomeapi.com.br/last/USD-BRL"
    )
    return new_client


@pytest.fixture()
def response_setup():
    new_client = ClientBuilder(
        endpoint="https://economia.awesomeapi.com.br/last/USD-BRL"
    )
    return new_client.get_api_data()


def test_constructor_raises():
    with pytest.raises(ValueError):
        ClientBuilder(endpoint="")

    with pytest.raises(ValueError):
        ClientBuilder(
            endpoint="https://economia.awesomeapi.com.br/last/USD-BRL", retries=-1
        )

    with pytest.raises(ValueError):
        ClientBuilder(
            endpoint="https://economia.awesomeapi.com.br/last/USD-BRL", initial_delay=-1
        )

    with pytest.raises(ValueError):
        ClientBuilder(
            endpoint="https://economia.awesomeapi.com.br/last/USD-BRL",
            connection_timeout=-1,
        )

    with pytest.raises(ValueError):
        ClientBuilder(
            endpoint="https://economia.awesomeapi.com.br/last/USD-BRL", retries=""
        )

    with pytest.raises(ValueError):
        ClientBuilder(
            endpoint="https://economia.awesomeapi.com.br/last/USD-BRL", initial_delay=""
        )

    with pytest.raises(ValueError):
        ClientBuilder(
            endpoint="https://economia.awesomeapi.com.br/last/USD-BRL",
            connection_timeout="",
        )


def test_constructor_with_param(client_setup):  # pylint: disable=redefined-outer-name
    expected_result = "https://economia.awesomeapi.com.br/last/USD-BRL"
    new_client = client_setup
    assert new_client.endpoint == expected_result


def test_response_to_json(client_setup):  # pylint: disable=redefined-outer-name
    new_client = client_setup
    response = new_client.get_api_data()  # pylint: disable=protected-access
    assert isinstance(response, dict)


def test_to_dataframe(response_setup):  # pylint: disable=redefined-outer-name
    df = ClientBuilder.api_to_dataframe(response_setup)
    assert isinstance(df, pd.DataFrame)
