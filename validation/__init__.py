"""
Módulo de Validação - Refatoração de Antipadrões.

Este módulo resolve dois antipadrões identificados:
1. Cut-and-Paste Programming - Decorator de validação centralizado
2. Input Kludge - Schemas de validação robustos

Autor: Fábio Amado (2501444)
UC: Arquitetura e Padrões de Software
"""

from validation.decorators import validate_request, validate_json
from validation.schemas import (
    SessionStartRequest,
    ChallengeRequest,
    ChallengeCompleteRequest,
    InteractionRequest,
    SessionEndRequest,
    AnalyticsRequest,
    ValidationError
)

__all__ = [
    # Decorators
    'validate_request',
    'validate_json',
    # Schemas
    'SessionStartRequest',
    'ChallengeRequest',
    'ChallengeCompleteRequest',
    'InteractionRequest',
    'SessionEndRequest',
    'AnalyticsRequest',
    'ValidationError'
]

__version__ = '1.0.0'
