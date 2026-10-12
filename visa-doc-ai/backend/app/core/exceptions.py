class VisaDocException(Exception):
    """Base exception for VisaDoc AI application."""
    def __init__(self, message: str, details: dict | None = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}


class SerpApiException(VisaDocException):
    """Raised when SerpApi communication fails or credentials are invalid."""
    pass


class SearchBudgetExhaustedException(VisaDocException):
    """Raised when maximum search budget is reached."""
    pass


class IngestionException(VisaDocException):
    """Raised when a webpage or PDF cannot be safely retrieved or parsed."""
    pass


class SecurityException(VisaDocException):
    """Raised when a security rule (SSRF, malicious scheme, injection) is violated."""
    pass


class VerificationException(VisaDocException):
    """Raised during requirement verification policy violations."""
    pass


class InvalidAgentOutputException(VisaDocException):
    """Raised when an AI agent produces unparseable or schema-violating output."""
    pass


class ResourceNotFoundException(VisaDocException):
    """Raised when an entity is not found."""
    pass
