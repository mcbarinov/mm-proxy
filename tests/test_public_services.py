"""Tests for public_services module."""

from urllib.parse import urlparse

from mm_proxy import check_proxy_ip_via_public_services


async def test_check_proxy_ip_http(http_proxy: str):
    """Verify HTTP proxy returns correct IP."""
    result = await check_proxy_ip_via_public_services(http_proxy)

    assert result.is_ok()
    expected_ip = urlparse(http_proxy).hostname
    assert result.value == expected_ip


async def test_check_proxy_ip_socks(socks_proxy: str):
    """Verify SOCKS5 proxy returns correct IP."""
    result = await check_proxy_ip_via_public_services(socks_proxy)

    assert result.is_ok()
    expected_ip = urlparse(socks_proxy).hostname
    assert result.value == expected_ip
