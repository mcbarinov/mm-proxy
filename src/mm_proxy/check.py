import time
from ipaddress import IPv4Address

from mm_http import http_request
from mm_result import Result


async def check_proxy_ip_plaintext(checker_url: str, proxy_url: str, timeout: float) -> Result[str]:
    """
    Check proxy IP via a plain-text IP service.

    The service must respond with a single IPv4 address in plain text.
    Examples: ipify.org, icanhazip.com, checkip.amazonaws.com

    Args:
        checker_url: URL of the IP check service
        proxy_url: Proxy URL (http://, socks5://, etc.)
        timeout: Request timeout in seconds

    Returns:
        Result[str] with IPv4 address or error
        extra: {"latency_ms": float, "checker_url": str}
    """
    start = time.perf_counter()
    resp = await http_request(checker_url, proxy=proxy_url, timeout=timeout)
    latency_ms = (time.perf_counter() - start) * 1000

    if resp.is_success() and resp.body:
        try:
            ip = str(IPv4Address(resp.body.strip()))
            return Result.ok(ip, extra={"latency_ms": latency_ms, "checker_url": checker_url})
        except ValueError:
            return Result.err(f"Invalid IPv4: {resp.body.strip()}", extra=resp.model_dump())
    return Result.err(resp.error_message or "Request failed", extra=resp.model_dump())
