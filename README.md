# mm-proxy

Async library for verifying proxy IP addresses via public IP check services.

## Quick Start

```python
from mm_proxy import check_proxy_ip_via_public_services

result = await check_proxy_ip_via_public_services("socks5://user:pass@1.2.3.4:1080", timeout=5)

if result.is_ok():
    print(result.value)                    # "1.2.3.4"
    print(result.extra["checker_url"])     # "https://api.ipify.org"
    print(result.extra["latency_ms"])      # 123.45
```

## API

### check_proxy_ip_via_public_services(proxy_url, *, timeout=10.0)

Queries all `PublicIPService` URLs in parallel, returns first successful result.

### check_proxy_ip_plaintext(checker_url, proxy_url, timeout)

Check proxy IP via a single plaintext IP service.

### PublicIPService

```python
class PublicIPService(StrEnum):
    IPIFY = "https://api.ipify.org"
    ICANHAZIP = "https://icanhazip.com"
    AMAZON = "https://checkip.amazonaws.com"
    IFCONFIG = "https://ifconfig.me/ip"
    IPINFO = "https://ipinfo.io/ip"
    IDENT = "https://v4.ident.me"
```
