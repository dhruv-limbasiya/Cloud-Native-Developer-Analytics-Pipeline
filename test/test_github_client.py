from unittest.mock import patch, Mock

from src.extract.github_client import GitHubClient


@patch("src.extract.github_client.requests.get")
def test_get_request(mock_get):

    mock_response = Mock()

    mock_response.status_code = 200

    mock_response.json.return_value = {
        "name": "tensorflow"
    }

    mock_response.headers = {
        "X-RateLimit-Remaining": "4999"
    }

    mock_get.return_value = mock_response

    client = GitHubClient()

    result = client.get("/repos/tensorflow/tensorflow")

    assert result["name"] == "tensorflow"


@patch("src.extract.github_client.requests.get")
def test_paginate(mock_get):

    page1 = Mock()
    page1.status_code = 200
    page1.headers = {
        "X-RateLimit-Remaining": "4999"
    }
    page1.json.return_value = [
        {"id": 1},
        {"id": 2}
    ]

    page2 = Mock()
    page2.status_code = 200
    page2.headers = {
        "X-RateLimit-Remaining": "4998"
    }
    page2.json.return_value = []

    mock_get.side_effect = [
        page1,
        page2
    ]

    client = GitHubClient()

    data = client.paginate(
        "/repositories",
        max_pages=2
    )

    assert len(data) == 2

    assert data[0]["id"] == 1

    assert data[1]["id"] == 2