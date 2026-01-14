"""Proxy list parsing utilities."""

from ipaddress import IPv4Address

PROXY_SCHEMES = ("http://", "https://", "socks4://", "socks5://")


def parse_proxy_list(text: str) -> list[str]:
    """
    Parse proxy entries from text.

    Supported formats:
        - URLs: http://, https://, socks4://, socks5:// (with optional auth and port)
        - IP:port: 192.168.1.1:8080
        - IP only: 192.168.1.1
        - hostname:port: proxy.example.com:8080

    Parsing behavior:
        - Lines starting with # are treated as comments and skipped
        - Inline comments (text after #) are stripped: "1.2.3.4:8080 # comment" → "1.2.3.4:8080"
        - Only the first token is used: "1.2.3.4:8080 extra text" → "1.2.3.4:8080"
        - Empty lines and invalid entries are skipped

    Args:
        text: Multi-line text containing proxy entries

    Returns:
        List of valid proxy entries
    """
    result = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        # Strip inline comment
        if "#" in line:
            line = line.split("#", 1)[0].strip()

        # Take first token only
        line = line.split()[0] if line else ""

        if line and _is_valid_proxy_entry(line):
            result.append(line)

    return result


def _is_valid_proxy_entry(line: str) -> bool:
    """Check if line is a valid proxy entry."""
    if line.startswith(PROXY_SCHEMES):
        return True

    if ":" in line:
        host, _, port = line.rpartition(":")
        if not port.isdigit():
            return False
        return _is_valid_ipv4(host) or _is_valid_hostname(host)

    return _is_valid_ipv4(line)


def _is_valid_ipv4(value: str) -> bool:
    """Check if value is a valid IPv4 address."""
    try:
        IPv4Address(value)
    except ValueError:
        return False
    return True


def _looks_like_ipv4(value: str) -> bool:
    """Check if value looks like an IPv4 address (4 numeric segments)."""
    parts = value.split(".")
    return len(parts) == 4 and all(p.isdigit() for p in parts)


def _is_valid_hostname(value: str) -> bool:
    """Check if value looks like a valid hostname."""
    if not value or len(value) > 253:
        return False

    if _looks_like_ipv4(value):
        return False

    labels = value.rstrip(".").split(".")
    if len(labels) < 2:
        return False

    for label in labels:
        if not label or len(label) > 63:
            return False
        if not all(c.isalnum() or c == "-" for c in label):
            return False
        if label.startswith("-") or label.endswith("-"):
            return False

    return True
