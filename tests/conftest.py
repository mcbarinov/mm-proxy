"""Test fixtures for proxy integration tests."""

import os
from urllib.parse import urlparse

import pytest
from dotenv import load_dotenv

load_dotenv()


def _get_proxy_url(env_var: str) -> str:
    value = os.environ.get(env_var)
    if not value:
        raise pytest.fail(f"{env_var} not set in .env file")
    parsed = urlparse(value)
    if not parsed.scheme or not parsed.hostname:
        raise pytest.fail(f"{env_var} is not a valid proxy URL: {value}")
    return value


@pytest.fixture
def http_proxy() -> str:
    return _get_proxy_url("HTTP_PROXY")


@pytest.fixture
def socks_proxy() -> str:
    return _get_proxy_url("SOCKS5_PROXY")
