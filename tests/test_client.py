import httpx
import pytest
import stringx


def test_default_base_url():
    with stringx.Client("test") as client:
        assert client.base_url.scheme == "https"
        assert client.base_url.host == "string-db.org"
        assert client.base_url.path == "/"


def test_custom_address():
    with stringx.Client("test", "https://example.com/api/v2") as client:
        assert client.base_url.host == "example.com"
        assert client.base_url.path == "/api/v2/"


def test_timeout():
    with stringx.Client("test") as client:
        assert client.timeout.connect == 5.0
        assert client.timeout.pool == 5.0
        assert client.timeout.read == 5.0
        assert client.timeout.write == 5.0


def test_mandatory_client_identity():
    with pytest.raises(TypeError, match="identity"):
        stringx.Client()  # type: ignore

    with pytest.raises(ValueError, match="Client identity must be a non-empty string"):
        stringx.Client(identity="")


def test_client_identity(test_client):
    assert test_client.identity == f"test client (python-stringx/{stringx.__version__})"


def test_caller_identity(test_client):
    assert test_client.params["caller_identity"] == test_client.identity


def test_custom_caller_identity():
    with stringx.Client(identity="random tool") as client:
        assert client.params["caller_identity"] == client.identity


def test_default_format(test_client):
    assert test_client.format == "json"


def test_map(httpx_mock, test_client):
    httpx_mock.add_response(
        url=httpx.URL(
            "https://string-db.org/api/json/get_string_ids",
            params={
                "identifiers": "some_identifier",
                "species": "7227",
                "limit": 1,
                "echo_query": True,
                "caller_identity": test_client.identity,
            },
        ),
        method="POST",
        json=True,
    )

    test_client.map(["some_identifier"], 7227)


def test_network(httpx_mock, test_client):
    httpx_mock.add_response(
        url=httpx.URL(
            "https://string-db.org/api/json/network",
            params={
                "identifiers": "id1",
                "species": "7227",
                "network_type": "functional",
                "show_query_node_labels": 0,
                "caller_identity": test_client.identity,
            },
        ),
        method="POST",
        json=True,
    )

    httpx_mock.add_response(
        url=httpx.URL(
            "https://string-db.org/api/json/network",
            params={
                "identifiers": "id1\rid2",
                "species": "7227",
                "required_score": 1,
                "network_type": "physical",
                "add_nodes": 2,
                "show_query_node_labels": 1,
                "caller_identity": test_client.identity,
            },
        ),
        method="POST",
        json=True,
    )

    test_client.network(["id1"], 7227)
    test_client.network(
        identifiers=["id1", "id2"],
        species=7227,
        required_score=1,
        network_type="physical",
        add_nodes=2,
        show_query_node_labels=True,
    )


def test_interaction_partners(httpx_mock, test_client):
    httpx_mock.add_response(
        url=httpx.URL(
            "https://string-db.org/api/json/interaction_partners",
            params={
                "identifiers": "id1\rid2",
                "species": "7227",
                "caller_identity": test_client.identity,
            },
        ),
        method="POST",
        json=True,
    )

    test_client.interaction_partners(["id1", "id2"], 7227)


@pytest.mark.parametrize("format", ["tsv", "tsv-no-header", "json", "xml"])
def test_homology(httpx_mock, test_client, format):
    identifiers = ["id1", "id2"]
    species = 1234

    httpx_mock.add_response()

    test_client.homology(identifiers, species, format=format)

    requested_url = httpx_mock.get_request().url

    assert requested_url.path == f"/api/{format}/homology"
    assert requested_url.params["identifiers"] == "\r".join(identifiers)
    assert requested_url.params["species"] == str(species)
    assert requested_url.params["caller_identity"] == test_client.identity


def test_version(httpx_mock, test_client):
    httpx_mock.add_response(
        url=httpx.URL("https://string-db.org/api/json/version"),
        method="GET",
        json=[
            {
                "string_version": "12.0",
                "stable_address": "https://version-12-0.string-db.org",
            }
        ],
    )

    test_client.version()
