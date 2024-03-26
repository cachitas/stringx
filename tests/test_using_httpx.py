import pytest
import httpx

import stringdb


@pytest.fixture(scope="session")
def api():
    with httpx.Client() as client:
        yield stringdb.API(client=client)


def test_api_with_httpx_client(api):
    assert api.client is not None


def test_api_current_version(api):
    assert api.version == stringdb.CURRENT_VERSION


def test_get_string_ids(api):
    identifiers = ["edin", "attc"]
    species = 7227

    response = api.get_string_ids(identifiers, species)

    for result in response:
        assert result["queryItem"] in identifiers
        assert result["ncbiTaxonId"] == species
        assert "stringId" in result.keys()


def test_get_interaction_partners(api):
    identifiers = ["7227.FBpp0074940", "7227.FBpp0297062"]
    species = 7227

    response = api.get_interaction_partners(identifiers, species)

    assert len(response) > 1


def test_get_interaction_partners_limited(api):
    identifiers = ["7227.FBpp0074940", "7227.FBpp0297062"]
    species = 7227
    limit = 1

    response = api.get_interaction_partners(identifiers, species, limit)

    assert len(response) == limit * len(identifiers)
