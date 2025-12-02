"""
Módulo de Sessões - Fábio Amado (2501444)

Integração do padrão Factory Method com analytics de sessões e interações.

Autor: Fábio Amado (2501444@estudante.uab.pt)
"""

from session_module.session_analytics import session_analytics, SessionAnalytics
from session_module.session_endpoints import register_session_routes

__all__ = [
    'session_analytics',
    'SessionAnalytics',
    'register_session_routes'
]

__version__ = '1.0.0'
__author__ = 'Fábio Amado (2501444)'
