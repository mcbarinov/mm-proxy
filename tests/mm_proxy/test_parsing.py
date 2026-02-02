"""Tests for parsing module."""

import pytest

from mm_proxy import parse_proxy_list


class TestParseProxyList:
    """Tests for parse_proxy_list function."""

    def test_empty_input(self):
        """Empty string returns empty list."""
        assert parse_proxy_list("") == []

    def test_whitespace_only(self):
        """Whitespace-only input returns empty list."""
        assert parse_proxy_list("   \n\n   \n") == []

    def test_comments_skipped(self):
        """Comment lines are skipped."""
        text = """
        # This is a comment
        # Another comment
        """
        assert parse_proxy_list(text) == []

    def test_http_url(self):
        """HTTP URLs are parsed."""
        assert parse_proxy_list("http://1.2.3.4:8080") == ["http://1.2.3.4:8080"]

    def test_https_url(self):
        """HTTPS URLs are parsed."""
        assert parse_proxy_list("https://1.2.3.4:443") == ["https://1.2.3.4:443"]

    def test_socks4_url(self):
        """SOCKS4 URLs are parsed."""
        assert parse_proxy_list("socks4://1.2.3.4:1080") == ["socks4://1.2.3.4:1080"]

    def test_socks5_url(self):
        """SOCKS5 URLs are parsed."""
        assert parse_proxy_list("socks5://1.2.3.4:1080") == ["socks5://1.2.3.4:1080"]

    def test_url_with_auth(self):
        """URLs with authentication are parsed."""
        assert parse_proxy_list("socks5://user:pass@1.2.3.4:1080") == ["socks5://user:pass@1.2.3.4:1080"]

    def test_ip_with_port(self):
        """IP:port format is parsed."""
        assert parse_proxy_list("192.168.1.1:8080") == ["192.168.1.1:8080"]

    def test_ip_only(self):
        """IP-only format is parsed."""
        assert parse_proxy_list("192.168.1.1") == ["192.168.1.1"]

    def test_hostname_with_port(self):
        """Hostname:port format is parsed."""
        assert parse_proxy_list("proxy.example.com:8080") == ["proxy.example.com:8080"]

    def test_invalid_ip_skipped(self):
        """Invalid IP addresses are skipped."""
        assert parse_proxy_list("999.999.999.999") == []
        assert parse_proxy_list("256.1.1.1:8080") == []

    def test_invalid_entries_skipped(self):
        """Invalid entries are skipped."""
        assert parse_proxy_list("not-a-proxy") == []
        assert parse_proxy_list("just-hostname") == []
        assert parse_proxy_list("192.168.1.1:abc") == []

    def test_mixed_input(self):
        """Mixed valid and invalid entries are correctly filtered."""
        text = """
        # Production proxies
        socks5://user:pass@1.2.3.4:1080
        http://proxy.example.com:8080
        192.168.1.1:3128
        10.0.0.1

        # Invalid (should be skipped)
        999.999.999.999
        invalid-entry
        """
        result = parse_proxy_list(text)
        assert result == [
            "socks5://user:pass@1.2.3.4:1080",
            "http://proxy.example.com:8080",
            "192.168.1.1:3128",
            "10.0.0.1",
        ]

    def test_preserves_original_format(self):
        """Whitespace is stripped but format preserved."""
        text = "  192.168.1.1:8080  "
        result = parse_proxy_list(text)
        assert result == ["192.168.1.1:8080"]

    @pytest.mark.parametrize(
        "valid_ip",
        [
            "0.0.0.0",
            "255.255.255.255",
            "127.0.0.1",
            "10.0.0.1",
            "172.16.0.1",
            "192.168.0.1",
        ],
    )
    def test_valid_ip_addresses(self, valid_ip):
        """Valid IP addresses are accepted."""
        assert parse_proxy_list(valid_ip) == [valid_ip]

    @pytest.mark.parametrize(
        "invalid_ip",
        [
            "256.0.0.0",
            "1.2.3.256",
            "1.2.3",
            "1.2.3.4.5",
            "abc.def.ghi.jkl",
        ],
    )
    def test_invalid_ip_addresses(self, invalid_ip):
        """Invalid IP addresses are rejected."""
        assert parse_proxy_list(invalid_ip) == []

    @pytest.mark.parametrize(
        "valid_hostname",
        [
            "proxy.example.com:8080",
            "a.b:80",
            "sub.domain.example.org:3128",
            "proxy-server.example.com:8080",
        ],
    )
    def test_valid_hostnames(self, valid_hostname):
        """Valid hostnames with port are accepted."""
        assert parse_proxy_list(valid_hostname) == [valid_hostname]

    @pytest.mark.parametrize(
        "invalid_hostname",
        [
            "localhost:8080",  # single label
            "-invalid.com:8080",  # starts with hyphen
            "invalid-.com:8080",  # ends with hyphen
        ],
    )
    def test_invalid_hostnames(self, invalid_hostname):
        """Invalid hostnames are rejected."""
        assert parse_proxy_list(invalid_hostname) == []

    def test_inline_comment_stripped(self):
        """Inline comments after # are stripped."""
        assert parse_proxy_list("192.168.1.1:8080 # production") == ["192.168.1.1:8080"]
        assert parse_proxy_list("https://1.2.3.4:443 # secure") == ["https://1.2.3.4:443"]

    def test_trailing_text_stripped(self):
        """Trailing text after proxy entry is stripped."""
        assert parse_proxy_list("192.168.1.1:8080 extra text") == ["192.168.1.1:8080"]
        assert parse_proxy_list("https://1.2.3.4:443 bla bla bla") == ["https://1.2.3.4:443"]
        assert parse_proxy_list("proxy.example.com:8080\tUS\tfast") == ["proxy.example.com:8080"]

    def test_inline_comment_and_trailing_text(self):
        """Both trailing text and inline comments are handled."""
        assert parse_proxy_list("192.168.1.1:8080 fast # production") == ["192.168.1.1:8080"]

    def test_only_comment_after_hash(self):
        """Lines with only comments are skipped."""
        assert parse_proxy_list("# just a comment") == []
        assert parse_proxy_list("  # indented comment") == []
