import httpx

import stringx


def test_default_base_url():
    with stringx.Client() as client:
        assert client.base_url.scheme == "https"
        assert client.base_url.host == "string-db.org"
        assert client.base_url.path == "/"


def test_custom_address():
    with stringx.Client("https://example.com/api/v2") as client:
        assert client.base_url.host == "example.com"
        assert client.base_url.path == "/api/v2/"


def test_timeout():
    with stringx.Client() as client:
        assert client.timeout.connect == 5.0
        assert client.timeout.pool == 5.0
        assert client.timeout.read == 5.0
        assert client.timeout.write == 5.0


def test_caller_identity():
    with stringx.Client() as client:
        assert client.params["caller_identity"] == stringx.DEFAULT_CALLER_IDENTITY


def test_custom_caller_identity():
    custom_identity = "random tool"
    with stringx.Client(identity=custom_identity) as client:
        assert client.params["caller_identity"] == custom_identity


def test_map_identifiers(httpx_mock):
    httpx_mock.add_response(
        url=httpx.URL(
            "https://string-db.org/api/json/get_string_ids",
            params={
                "identifiers": "some_identifier",
                "species": "7227",
                "limit": 1,
                "echo_query": True,
                "caller_identity": stringx.DEFAULT_CALLER_IDENTITY,
            },
        ),
        method="POST",
        json=True,
    )

    with stringx.Client() as client:
        client.map_identifiers(["some_identifier"], 7227)


def test_interaction_partners(httpx_mock):
    httpx_mock.add_response(
        url=httpx.URL(
            "https://string-db.org/api/json/interaction_partners",
            params={
                "identifiers": "id1\rid2",
                "species": "7227",
                "caller_identity": stringx.DEFAULT_CALLER_IDENTITY,
            },
        ),
        method="POST",
        json=True,
    )

    with stringx.Client() as client:
        client.interaction_partners(["id1", "id2"], 7227)
