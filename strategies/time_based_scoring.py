"""
Estratégia de Pontuação Baseada em Tempo

Calcula pontos baseado na velocidade de resposta.
Quanto mais rápido, mais pontos.
"""
from typing import Dict, Any
from strategies.scoring_strategy import ScoringStrategy


class TimeBasedScoringStrategy(ScoringStrategy):
    """
    Concrete Strategy: Pontuação baseada em tempo.

    Recompensa respostas rápidas com mais pontos.
    Integra-se com TimedDecorator para aproveitar métricas de tempo.
    """

    def calculate_score(self, context: Dict[str, Any]) -> int:
        """
        Calcula pontuação baseada no tempo de resposta.

        Fórmula:
        - <= 25% do tempo: 100 pontos
        - <= 50% do tempo: 75 pontos
        - <= 75% do tempo: 50 pontos
        - > 75% do tempo: 25 pontos
        - Timeout ou incorreto: 0 pontos

        Args:
            context: Deve conter 'time_taken', 'time_limit', 'is_correct'

        Returns:
            Pontuação de 0 a 100
        """
        time_taken = context.get('time_taken', 0)
        time_limit = context.get('time_limit', 30)
        is_correct = context.get('is_correct', False)

        # Resposta incorreta = 0 pontos
        if not is_correct:
            return 0

        # Timeout = 0 pontos
        if time_taken >= time_limit:
            return 0

        # Calcular percentagem de tempo usado
        time_percentage = (time_taken / time_limit) * 100

        if time_percentage <= 25:
            return 100
        elif time_percentage <= 50:
            return 75
        elif time_percentage <= 75:
            return 50
        else:
            return 25

    def get_strategy_name(self) -> str:
        return "time_based"
