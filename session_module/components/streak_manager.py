"""
Gestor de Streaks - Componente SRP.

Responsabilidade Única: Gerir dias consecutivos e streaks de acertos.

Autor: Fábio Amado (2501444)
"""
from typing import Dict
from datetime import datetime


class StreakManager:
    """
    Gere streaks de dias consecutivos e acertos.

    Responsabilidades:
    - Calcular dias consecutivos de jogo
    - Gerir streak de acertos em sessão
    - Atualizar best_streak do utilizador
    """

    def update_consecutive_days(self, user_stats: Dict) -> None:
        """
        Atualiza contagem de dias consecutivos.

        Args:
            user_stats: Estatísticas do utilizador (modificado in-place)
        """
        today = datetime.now().date()

        # Adicionar data de hoje
        if today not in user_stats['play_dates']:
            user_stats['play_dates'].append(today)

        # Calcular dias consecutivos
        if user_stats['last_play_date']:
            last_date = datetime.fromisoformat(
                user_stats['last_play_date']
            ).date()
            diff = (today - last_date).days

            if diff == 1:
                # Dia consecutivo
                user_stats['consecutive_days'] += 1
            elif diff > 1:
                # Quebrou sequência
                user_stats['consecutive_days'] = 1
        else:
            user_stats['consecutive_days'] = 1

        user_stats['last_play_date'] = today.isoformat()

    def update_session_streak(self, session: Dict,
                             is_correct: bool) -> int:
        """
        Atualiza streak de acertos na sessão.

        Args:
            session: Dados da sessão (modificado in-place)
            is_correct: Se resposta estava correta

        Returns:
            Streak atual
        """
        if is_correct:
            session['current_streak'] += 1
        else:
            session['current_streak'] = 0

        return session['current_streak']

    def check_best_streak(self, user_stats: Dict,
                         current_streak: int) -> bool:
        """
        Verifica e atualiza best_streak se necessário.

        Args:
            user_stats: Estatísticas do utilizador (modificado in-place)
            current_streak: Streak atual

        Returns:
            True se foi um novo recorde
        """
        if current_streak > user_stats.get('best_streak', 0):
            user_stats['best_streak'] = current_streak
            return True
        return False
