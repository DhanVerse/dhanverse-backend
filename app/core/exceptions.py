class DhanVerseException(Exception):
    """Base exception for all application exceptions."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class ResourceNotFoundError(DhanVerseException):
    """Raised when requested resource is not found."""
    pass


class DuplicateResourceError(DhanVerseException):
    """Raised when duplicate resource exists."""
    pass


class BusinessValidationError(DhanVerseException):
    """Raised when business validation fails."""
    pass