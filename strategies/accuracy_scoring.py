"""
Estratégia de Pontuação Baseada em Precisão

Calcula pontos baseado no número de tentativas.
Primeira tentativa correta = máxima pontuação.
"""
from typing import Dict, Any
from strategies.scoring_strategy import ScoringStrategy


class AccuracyScoringStrategy(ScoringStrategy):
    """
    Concrete Strategy: Pontuação baseada em precisão.

    Recompensa acertar na primeira tentativa.
    Penaliza múltiplas tentativas.
    """

    def calculate_score(self, context: Dict[str, Any]) -> int:
        """
        Calcula pontuação baseada no número de tentativas.

        Fórmula:
        - 1ª tentativa correta: 100 pontos
        - 2ª tentativa correta: 60 pontos
        - 3ª tentativa correta: 30 pontos
        - 4+ tentativas ou incorreto: 0 pontos

        Args:
            context: Deve conter 'attempts' e 'is_correct'

        Returns:
            Pontuação de 0 a 100
        """
        attempts = context.get('attempts', 1)
        is_correct = context.get('is_correct', False)

        # Resposta incorreta = 0 pontos
        if not is_correct:
            return 0

        # Calcular pontos baseado em tentativas
        if attempts == 1:
            return 100
        elif attempts == 2:
            return 60
        elif attempts == 3:
            return 30
        else:
            return 0

    def get_strategy_name(self) -> str:
        return "accuracy_based"
