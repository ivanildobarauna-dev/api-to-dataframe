import pytest
import requests
import responses

from api_to_dataframe.models.get_data import GetData
from api_to_dataframe.controller.client_builder import ClientBuilder


def test_to_dataframe():
    with pytest.raises(TypeError):
        GetData.to_dataframe("")


@responses.activate
def test_to_emp_dataframe():
    endpoint = "https://api.exemplo.com"
    expected_response = {}

    responses.add(responses.GET, endpoint,
                  json=expected_response, status=200)

    client = ClientBuilder(endpoint=endpoint)
    response = client.get_api_data()

    with pytest.raises(ValueError):
        GetData.to_dataframe(response)


@responses.activate
def test_http_error():
    endpoint = "https://api.exemplo.com"
    expected_response = {}

    responses.add(responses.GET, endpoint,
                  json=expected_response, status=400)

    with ((pytest.raises(requests.exceptions.HTTPError))):
        GetData.get_response(
            endpoint=endpoint,
            headers={},
            connection_timeout=10)


@responses.activate
def test_timeout_error():
    endpoint = "https://api.exemplo.com"

    responses.add(responses.GET, endpoint, body=requests.exceptions.Timeout())

    with pytest.raises(requests.exceptions.Timeout):
        GetData.get_response(
            endpoint=endpoint,
            headers={},
            connection_timeout=10)


@responses.activate
def test_request_exception():
    endpoint = "https://api.exemplo.com"

    expected_response = {}

    responses.add(responses.GET, endpoint,
                  json=expected_response, status=500)

    with pytest.raises(requests.exceptions.RequestException):
        GetData.get_response(
            endpoint=endpoint,
            headers={},
            connection_timeout=10)
