import pytest

from smsclient import SMSClient


@pytest.fixture
def client() -> SMSClient:
    return SMSClient("test-api-key")
