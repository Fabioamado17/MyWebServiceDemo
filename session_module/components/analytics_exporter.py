"""
Exportador de Analytics - Componente SRP.

Responsabilidade Única: Formatar dados para exportação.

Autor: Fábio Amado (2501444)
"""
from typing import Dict, Optional
from datetime import datetime


class AnalyticsExporter:
    """
    Exporta analytics em formato compatível com Inven!RA.

    Responsabilidades:
    - Formatar dados para Inven!RA
    - Incluir metadados de timestamp
    - Garantir estrutura consistente
    """

    ACTIVITY_ID = 'dia-noite-animals'

    def export_for_invenira(self, user_id: str,
                           user_stats: Optional[Dict]) -> Dict:
        """
        Exporta analytics em formato Inven!RA.

        Args:
            user_id: Identificador do utilizador
            user_stats: Estatísticas do utilizador (ou None)

        Returns:
            Dados formatados para Inven!RA
        """
        if user_stats is None:
            return self._empty_export(user_id)

        return {
            'studentId': user_id,
            'activityId': self.ACTIVITY_ID,
            'sessionMetrics': {
                'totalSessions': user_stats['total_sessions'],
                'totalPlayTime': user_stats['total_play_time'],
                'totalChallenges': user_stats['total_challenges'],
                'totalInteractions': user_stats['total_interactions'],
                'consecutiveDays': user_stats['consecutive_days'],
                'avgSessionTime': self._calculate_avg_session_time(user_stats),
                # Strategy Pattern
                'totalScore': user_stats.get('total_score', 0),
                'avgScore': round(user_stats.get('avg_score', 0.0), 2),
                'bestStreak': user_stats.get('best_streak', 0)
            },
            'timestamp': datetime.now().isoformat()
        }

    def _empty_export(self, user_id: str) -> Dict:
        """Retorna estrutura vazia para utilizador sem dados."""
        return {
            'studentId': user_id,
            'activityId': self.ACTIVITY_ID,
            'sessionMetrics': {},
            'timestamp': datetime.now().isoformat()
        }

    def _calculate_avg_session_time(self, user_stats: Dict) -> float:
        """Calcula tempo médio por sessão."""
        if user_stats['total_sessions'] > 0:
            return user_stats['total_play_time'] / user_stats['total_sessions']
        return 0
