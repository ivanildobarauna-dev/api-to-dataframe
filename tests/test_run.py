import pytest
import pandas as pd
import api_to_dataframe as api_to_dataframe


@pytest.fixture()
def setup():
    new_client = api_to_dataframe.ClientBuilder(endpoint="https://economia.awesomeapi.com.br/last/USD-BRL")
    return new_client


def test_constructor_without_param():
    with pytest.raises(ValueError):
        new_client = api_to_dataframe.ClientBuilder(endpoint="")


def test_constructor_with_param(setup):
    expected_result = "https://economia.awesomeapi.com.br/last/USD-BRL"
    new_client = setup
    assert new_client.endpoint == expected_result


def test_response_to_json(setup):
    new_client = setup
    response = new_client._response_to_json()
    assert isinstance(response, dict)


def test_to_dataframe(setup):
    new_client = setup
    df = new_client.to_dataframe()
    assert isinstance(df, pd.DataFrame)
