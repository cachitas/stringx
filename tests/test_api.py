import stringdb


def test_default_version():
    api = stringdb.API()

    latest_version = next(iter(stringdb.API.VERSION_ADDRESSES))

    assert api.version == latest_version


def test_older_versions():
    for version in ["10.0", "10.5", "11.0", "11.0b", "11.5"]:
        api = stringdb.API(version)
        assert api.version == version


def test_default_url():
    api = stringdb.API()
    assert api.api_url == "https://string-db.org/api"


def test_clientless_api():
    api = stringdb.API()
    assert api.client is None

    result = api._get("endpoint", params=dict(param1="value", param2=9000))

    assert len(result) == 2

    url, params = result

    assert url == api.api_url + "/json/endpoint"
    assert params["param1"] == "value"
    assert params["param2"] == 9000


def test_get_string_ids():
    api = stringdb.API()

    url, params = api.get_string_ids(["edin"], species=7227)

    assert url == api.api_url + "/json/get_string_ids"
    assert params["identifiers"] == "edin"
    assert params["species"] == 7227
    assert params["caller_identity"] == "stringdb.api"
