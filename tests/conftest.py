import pytest

from pysmscenter import SMSClient


@pytest.fixture
def client() -> SMSClient:
    return SMSClient("test-api-key")
