import ipaddress
import socket
from urllib.parse import urlparse
from app.core.exceptions import SecurityException


BLOCKED_HOSTNAMES = {"localhost", "127.0.0.1", "0.0.0.0", "::1", "metadata.google.internal"}


def is_safe_url(url: str) -> bool:
    """
    Validates whether a URL is safe to retrieve from backend ingestion service.
    Protects against SSRF and non-HTTP schemes.
    """
    if not url or not isinstance(url, str):
        return False

    parsed = urlparse(url)
    if parsed.scheme.lower() not in {"http", "https"}:
        return False

    hostname = parsed.hostname
    if not hostname:
        return False

    hostname_lower = hostname.lower()
    if hostname_lower in BLOCKED_HOSTNAMES:
        return False

    # Check if host is direct IP address
    try:
        ip = ipaddress.ip_address(hostname_lower)
        if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_multicast or ip.is_reserved:
            return False
    except ValueError:
        # Not a raw IP literal; hostname is domain name
        pass

    # Resolve domain to test resolved IP if not mock/test
    try:
        resolved_ip = socket.gethostbyname(hostname)
        ip = ipaddress.ip_address(resolved_ip)
        if ip.is_private or ip.is_loopback or ip.is_link_local:
            return False
    except Exception:
        # If DNS fails, we allow it to proceed to HTTP fetch which will handle connection error
        pass

    return True


def validate_url_or_raise(url: str) -> None:
    if not is_safe_url(url):
        raise SecurityException(f"URL violates security boundary or SSRF policy: {url}")
