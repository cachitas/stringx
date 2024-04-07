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


@pytest.mark.parametrize("format", ["tsv", "tsv-no-header", "json", "xml"])
def test_map(httpx_mock, test_client, format):
    httpx_mock.add_response(
        url=httpx.URL(
            f"https://string-db.org/api/{format}/get_string_ids",
            params={
                "identifiers": "some_identifier",
                "species": 1234,
                "limit": 1,
                "echo_query": True,
                "caller_identity": test_client.identity,
            },
        ),
        method="POST",
    )

    test_client.map(["some_identifier"], 1234, format=format)


@pytest.mark.parametrize(
    "format", ["tsv", "tsv-no-header", "json", "xml", "psi-mi", "psi-mi-tab"]
)
def test_network(httpx_mock, test_client, format):
    identifiers = ["id1"]
    species = 1234

    httpx_mock.add_response(
        url=httpx.URL(
            f"https://string-db.org/api/{format}/network",
            params={
                "identifiers": identifiers,
                "species": species,
                "network_type": "functional",
                "show_query_node_labels": 0,
                "caller_identity": test_client.identity,
            },
        ),
        method="POST",
    )

    httpx_mock.add_response(
        url=httpx.URL(
            f"https://string-db.org/api/{format}/network",
            params={
                "identifiers": identifiers,
                "species": species,
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

    test_client.network(identifiers, species, format=format)
    test_client.network(
        identifiers=identifiers,
        species=species,
        required_score=1,
        network_type="physical",
        add_nodes=2,
        show_query_node_labels=True,
        format=format,
    )


@pytest.mark.parametrize(
    "format", ["tsv", "tsv-no-header", "json", "xml", "psi-mi", "psi-mi-tab"]
)
def test_interaction_partners(httpx_mock, test_client, format):
    identifiers = ["id1"]
    species = 1234

    httpx_mock.add_response(
        url=httpx.URL(
            f"https://string-db.org/api/{format}/interaction_partners",
            params={
                "identifiers": identifiers,
                "species": species,
                "caller_identity": test_client.identity,
            },
        ),
        method="POST",
        json=True,
    )

    test_client.interaction_partners(identifiers, species, format=format)


@pytest.mark.parametrize("format", ["tsv", "tsv-no-header", "json", "xml"])
def test_homology(httpx_mock, test_client, format):
    identifiers = ["id1"]
    species = 1234

    httpx_mock.add_response(
        url=httpx.URL(
            f"https://string-db.org/api/{format}/homology",
            params={
                "identifiers": identifiers,
                "species": species,
                "caller_identity": test_client.identity,
            },
        ),
    )

    test_client.homology(identifiers, species, format=format)


@pytest.mark.parametrize("format", ["tsv", "tsv-no-header", "json", "xml"])
def test_enrichment(httpx_mock, test_client, format):
    identifiers = ["id1"]
    background_identifiers = ["id2"]
    species = 1234

    httpx_mock.add_response(
        url=httpx.URL(
            f"https://string-db.org/api/{format}/enrichment",
            params={
                "identifiers": identifiers,
                "background_string_identifiers": background_identifiers,
                "species": species,
                "caller_identity": test_client.identity,
            },
        ),
    )

    test_client.enrichment(
        identifiers,
        species,
        background_identifiers=background_identifiers,
        format=format,
    )


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
