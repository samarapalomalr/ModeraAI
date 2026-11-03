"""Exceções de domínio. A camada de API as traduz para respostas HTTP."""


class InvalidPostURLError(ValueError):
    """URL de post inválida ou de plataforma não suportada."""


class PostDataNotFoundError(Exception):
    """Não foi possível obter os dados da publicação."""


class AuditNotFoundError(Exception):
    """Auditoria inexistente."""
