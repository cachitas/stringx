import pytest
import stringx


@pytest.fixture(scope="session")
def test_client():
    with stringx.Client(identity="test client") as client:
        yield client
