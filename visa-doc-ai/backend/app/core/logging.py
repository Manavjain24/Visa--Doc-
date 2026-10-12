import logging
import re
from typing import Any

SENSITIVE_PATTERNS = [
    re.compile(r'(api[_-]?key[\s:=]+)[\'"]?([a-zA-Z0-9_\-\.]{8,})[\'"]?', re.IGNORECASE),
    re.compile(r'(authorization[\s:=]+Bearer\s+)[a-zA-Z0-9_\-\.]+', re.IGNORECASE),
    re.compile(r'(password[\s:=]+)[\'"]?[^\s\'"]+[\'"]?', re.IGNORECASE),
    re.compile(r'(\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b)'),  # email scrub
    re.compile(r'(\b[A-Z0-9]{8,9}\b)'), # passport-like patterns
]


class SanitizingFormatter(logging.Formatter):
    """Formats log records while scrubbing API keys and PII."""

    def format(self, record: logging.LogRecord) -> str:
        msg = super().format(record)
        for pattern in SENSITIVE_PATTERNS:
            msg = pattern.sub(r'\1[REDACTED]', msg)
        return msg


def setup_logging(level: str = "INFO") -> logging.Logger:
    logger = logging.getLogger("visadoc")
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    logger.handlers.clear()

    handler = logging.StreamHandler()
    formatter = SanitizingFormatter(
        "%(asctime)s [%(levelname)s] %(name)s (%(module)s): %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


logger = setup_logging()
