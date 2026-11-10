class DomainError(Exception):
    """Base dos erros de negócio. A camada API os traduz para HTTP."""


class InvalidPostURLError(DomainError):
    pass


class PostDataUnavailableError(DomainError):
    pass


class AuditNotFoundError(DomainError):
    pass


class InvalidMediaURLError(DomainError):
    pass


class MediaUnavailableError(DomainError):
    pass


class EmailAlreadyRegisteredError(DomainError):
    pass


class InvalidCredentialsError(DomainError):
    pass


class InvalidTokenError(DomainError):
    pass
