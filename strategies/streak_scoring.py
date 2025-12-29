"""
Estratégia de Pontuação Baseada em Sequência

Calcula pontos baseado em acertos consecutivos (streak).
Recompensa consistência.
"""
from typing import Dict, Any
from strategies.scoring_strategy import ScoringStrategy


class StreakScoringStrategy(ScoringStrategy):
    """
    Concrete Strategy: Pontuação baseada em streak.

    Recompensa sequências de acertos consecutivos.
    Quanto maior o streak, mais pontos bónus.
    """

    def calculate_score(self, context: Dict[str, Any]) -> int:
        """
        Calcula pontuação baseada em streak de acertos.

        Fórmula:
        - Base: 50 pontos (se correto)
        - Bónus por streak:
          * 2-3 consecutivos: +10 pontos
          * 4-5 consecutivos: +20 pontos
          * 6-9 consecutivos: +30 pontos
          * 10+ consecutivos: +50 pontos

        Args:
            context: Deve conter 'streak' e 'is_correct'

        Returns:
            Pontuação de 0 a 100
        """
        streak = context.get('streak', 0)
        is_correct = context.get('is_correct', False)

        # Resposta incorreta = 0 pontos (quebra streak)
        if not is_correct:
            return 0

        # Pontos base por acertar
        base_score = 50

        # Calcular bónus de streak
        if streak >= 10:
            bonus = 50
        elif streak >= 6:
            bonus = 30
        elif streak >= 4:
            bonus = 20
        elif streak >= 2:
            bonus = 10
        else:
            bonus = 0

        return min(base_score + bonus, 100)

    def get_strategy_name(self) -> str:
        return "streak_based"
