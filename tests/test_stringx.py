import pytest
import stringx

stringx.identity = "test client"


def test_invalid_identity():
    stringx.identity = ""

    with pytest.raises(ValueError):
        stringx.network(["7227.FBpp0074940"], species=7227)


def test_valid_identity(httpx_mock):
    httpx_mock.add_response(json={})

    stringx.identity = "someone"

    stringx.network(["7227.FBpp0074940"], species=7227)

    assert (
        httpx_mock.get_request().url.params["caller_identity"]
        == f"{stringx.identity} (python-stringx/{stringx.__version__})"
    )


def test_map(httpx_mock):
    httpx_mock.add_response(json=True)
    stringx.map(["id1"], 1234)
    stringx.map(["id1"], 1234, limit=2)
    stringx.map(["id1"], 1234, echo_query=False)


def test_network(httpx_mock):
    httpx_mock.add_response(json=True)
    stringx.network(["id1"], 1234)
    stringx.network(["id1"], 1234, required_score=1)
    stringx.network(["id1"], 1234, network_type="other")
    stringx.network(["id1"], 1234, add_nodes=50)
    stringx.network(["id1"], 1234, show_query_node_labels=True)


def test_interaction_partners(httpx_mock):
    httpx_mock.add_response(json=True)
    stringx.interaction_partners(["id1"], 1234)
    stringx.interaction_partners(["id1"], 1234, limit=10)


def test_homology(httpx_mock):
    httpx_mock.add_response(json=True)
    stringx.homology(["id1"], 1234)


def test_enrichment(httpx_mock):
    httpx_mock.add_response(json=True)
    stringx.enrichment(["id1"], 1234)
    stringx.enrichment(["id1"], 1234, background_identifiers=["id2"])
