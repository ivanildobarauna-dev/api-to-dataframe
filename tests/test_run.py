import pytest
import src.api_to_dataframe as apitodf


def test_constructor_without_param():
    with pytest.raises(ValueError):
        new_client = apitodf.ClientBuilder(endpoint="")


@pytest.fixture()
def test_constructor_with_param():
    expected_result = "param1"
    new_client = apitodf.ClientBuilder(endpoint=expected_result)
    assert new_client.endpoint == expected_result
    return new_client


def test_response_to_json_with_valid_endpoint(test_constructor_with_param):
    pass
