"""
Componentes do Módulo de Sessões - Refatoração Blob/God Object.

Este módulo decompõe a classe monolítica SessionAnalytics em
componentes especializados com responsabilidades únicas:

1. SessionManager - Gestão de sessões (criar, terminar)
2. EventTracker - Registo de eventos (desafios, interações)
3. StatisticsCalculator - Cálculo de estatísticas
4. StreakManager - Gestão de dias consecutivos
5. AnalyticsExporter - Exportação para Inven!RA

ANTIPADRÃO RESOLVIDO: Blob/God Object
- Antes: SessionAnalytics com 6+ responsabilidades (464 linhas)
- Depois: 5 classes especializadas, cada uma com ~50-80 linhas

Autor: Fábio Amado (2501444)
"""

from session_module.components.session_manager import SessionManager
from session_module.components.event_tracker import EventTracker
from session_module.components.statistics_calculator import StatisticsCalculator
from session_module.components.streak_manager import StreakManager
from session_module.components.analytics_exporter import AnalyticsExporter

__all__ = [
    'SessionManager',
    'EventTracker',
    'StatisticsCalculator',
    'StreakManager',
    'AnalyticsExporter'
]
