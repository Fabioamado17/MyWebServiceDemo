"""
Estratégia de Pontuação Baseada em Dificuldade

Calcula pontos ajustados pela dificuldade do desafio.
Desafios mais difíceis valem mais pontos.
"""
from typing import Dict, Any
from strategies.scoring_strategy import ScoringStrategy


class DifficultyBasedScoringStrategy(ScoringStrategy):
    """
    Concrete Strategy: Pontuação baseada em dificuldade.

    Ajusta pontuação de acordo com o nível de dificuldade.
    Desafios mais difíceis recompensam mais pontos.
    """

    def calculate_score(self, context: Dict[str, Any]) -> int:
        """
        Calcula pontuação baseada em dificuldade.

        Fórmula:
        - Dificuldade 1 (fácil): 40 pontos base
        - Dificuldade 2: 60 pontos base
        - Dificuldade 3 (médio): 80 pontos base
        - Dificuldade 4: 90 pontos base
        - Dificuldade 5 (difícil): 100 pontos base

        Args:
            context: Deve conter 'difficulty' (1-5) e 'is_correct'

        Returns:
            Pontuação de 0 a 100
        """
        difficulty = context.get('difficulty', 3)
        is_correct = context.get('is_correct', False)

        # Resposta incorreta = 0 pontos
        if not is_correct:
            return 0

        # Mapear dificuldade para pontuação
        difficulty_scores = {
            1: 40,  # Fácil
            2: 60,
            3: 80,  # Médio
            4: 90,
            5: 100  # Difícil
        }

        return difficulty_scores.get(difficulty, 80)

    def get_strategy_name(self) -> str:
        return "difficulty_based"
