"""
Calculador de Estatísticas - Componente SRP.

Responsabilidade Única: Calcular e agregar estatísticas.

Autor: Fábio Amado (2501444)
"""
from typing import Dict, List


class StatisticsCalculator:
    """
    Calcula estatísticas de sessões e utilizadores.

    Responsabilidades:
    - Calcular sumário de sessão
    - Agregar estatísticas de utilizador
    - Calcular médias e totais
    """

    def __init__(self):
        """Inicializa o calculador com stats de utilizadores."""
        # {user_id: {estatísticas}}
        self.user_stats: Dict[str, Dict] = {}

    def init_user_stats(self, user_id: str) -> None:
        """
        Inicializa estatísticas para um novo utilizador.

        Args:
            user_id: Identificador do utilizador
        """
        if user_id not in self.user_stats:
            self.user_stats[user_id] = {
                'total_sessions': 0,
                'total_play_time': 0,
                'total_challenges': 0,
                'total_interactions': 0,
                'consecutive_days': 0,
                'last_play_date': None,
                'play_dates': [],
                # Strategy Pattern
                'total_score': 0,
                'best_streak': 0,
                'avg_score': 0.0
            }

    def increment_session_count(self, user_id: str) -> None:
        """Incrementa contador de sessões do utilizador."""
        self.user_stats[user_id]['total_sessions'] += 1

    def increment_challenge_count(self, user_id: str) -> None:
        """Incrementa contador de desafios do utilizador."""
        self.user_stats[user_id]['total_challenges'] += 1

    def increment_interaction_count(self, user_id: str) -> None:
        """Incrementa contador de interações do utilizador."""
        self.user_stats[user_id]['total_interactions'] += 1

    def update_play_time(self, user_id: str, duration: float) -> None:
        """Adiciona tempo de jogo ao total do utilizador."""
        self.user_stats[user_id]['total_play_time'] += duration

    def update_score_stats(self, user_id: str,
                          session_score: int,
                          current_streak: int) -> None:
        """
        Atualiza estatísticas de pontuação.

        Args:
            user_id: Identificador do utilizador
            session_score: Pontuação da sessão
            current_streak: Streak atual
        """
        stats = self.user_stats[user_id]
        stats['total_score'] += session_score

        # Atualizar best streak
        if current_streak > stats['best_streak']:
            stats['best_streak'] = current_streak

        # Recalcular média
        total_challenges = stats['total_challenges']
        if total_challenges > 0:
            stats['avg_score'] = stats['total_score'] / total_challenges

    def calculate_session_summary(self, session: Dict) -> Dict:
        """
        Calcula sumário de uma sessão.

        Args:
            session: Dados da sessão

        Returns:
            Sumário da sessão
        """
        # Tempo médio por desafio
        avg_challenge_time = 0
        if session['challenge_times']:
            total_time = sum(
                ct['duration'] for ct in session['challenge_times']
            )
            avg_challenge_time = total_time / len(session['challenge_times'])

        # Contagem de interações por tipo
        interaction_counts = {}
        for interaction in session['interactions']:
            itype = interaction['type']
            interaction_counts[itype] = interaction_counts.get(itype, 0) + 1

        return {
            'session_id': session['session_id'],
            'user_id': session['user_id'],
            'duration': session['duration'],
            'challenges_attempted': session['challenges_attempted'],
            'total_interactions': len(session['interactions']),
            'interaction_breakdown': interaction_counts,
            'avg_challenge_time': round(avg_challenge_time, 2),
            'challenge_times': session['challenge_times'],
            'start_time': session['start_time'],
            'end_time': session['end_time'],
            'active': session['active'],
            # Strategy Pattern
            'total_score': session.get('total_score', 0),
            'current_streak': session.get('current_streak', 0),
            'scores': session.get('scores', [])
        }

    def calculate_user_report(self, user_id: str,
                             sessions_data: List[Dict]) -> Dict:
        """
        Calcula relatório completo de um utilizador.

        Args:
            user_id: Identificador do utilizador
            sessions_data: Lista de sumários de sessões

        Returns:
            Relatório agregado
        """
        if user_id not in self.user_stats:
            return {
                'user_id': user_id,
                'total_sessions': 0,
                'sessions': []
            }

        stats = self.user_stats[user_id]

        return {
            'user_id': user_id,
            'total_sessions': stats['total_sessions'],
            'total_play_time': stats['total_play_time'],
            'avg_session_time': (
                stats['total_play_time'] / stats['total_sessions']
                if stats['total_sessions'] > 0 else 0
            ),
            'total_challenges': stats['total_challenges'],
            'total_interactions': stats['total_interactions'],
            'consecutive_days': stats['consecutive_days'],
            # Strategy Pattern
            'total_score': stats.get('total_score', 0),
            'avg_score': round(stats.get('avg_score', 0.0), 2),
            'best_streak': stats.get('best_streak', 0),
            'sessions': sessions_data
        }
