"""Public IP check services."""

import asyncio
from enum import StrEnum

from mm_result import Result

from mm_proxy.check import check_proxy_ip_plaintext


class PublicIPService(StrEnum):
    """Public services that return your IP address as plain text."""

    IPIFY = "https://api.ipify.org"
    ICANHAZIP = "https://icanhazip.com"
    AMAZON = "https://checkip.amazonaws.com"
    IFCONFIG = "https://ifconfig.me/ip"
    IPINFO = "https://ipinfo.io/ip"
    IDENT = "https://v4.ident.me"


async def check_proxy_ip_via_public_services(proxy_url: str, *, timeout: float = 10.0) -> Result[str]:
    """Check proxy IP using all public services in parallel, return first success."""
    tasks = [asyncio.create_task(check_proxy_ip_plaintext(service, proxy_url, timeout)) for service in PublicIPService]

    try:
        for coro in asyncio.as_completed(tasks):
            result = await coro
            if result.is_ok():
                return result
    finally:
        for t in tasks:
            t.cancel()

    return Result.err("All IP check services failed")
