"""
Estratégia de Pontuação Composta

Combina múltiplas estratégias com pesos configuráveis.
Permite criar sistemas de pontuação complexos.
"""
from typing import Dict, Any, List, Tuple
from strategies.scoring_strategy import ScoringStrategy


class CompositeScoringStrategy(ScoringStrategy):
    """
    Concrete Strategy: Pontuação composta.

    Combina múltiplas estratégias com pesos personalizados.
    Permite criar sistemas híbridos de pontuação.

    Exemplo:
        strategy = CompositeScoringStrategy([
            (TimeBasedScoringStrategy(), 0.5),    # 50% peso
            (AccuracyScoringStrategy(), 0.3),      # 30% peso
            (StreakScoringStrategy(), 0.2)         # 20% peso
        ])
    """

    def __init__(self, strategies: List[Tuple[ScoringStrategy, float]]):
        """
        Inicializa estratégia composta.

        Args:
            strategies: Lista de tuplas (estratégia, peso)
                       Os pesos devem somar 1.0
        """
        self.strategies = strategies

        # Validar pesos
        total_weight = sum(weight for _, weight in strategies)
        if not (0.99 <= total_weight <= 1.01):  # Tolerância para erros de float
            raise ValueError(f"Pesos devem somar 1.0, obtido: {total_weight}")

    def calculate_score(self, context: Dict[str, Any]) -> int:
        """
        Calcula pontuação combinando múltiplas estratégias.

        Args:
            context: Contexto com todos os dados necessários

        Returns:
            Pontuação ponderada de 0 a 100
        """
        total_score = 0.0

        for strategy, weight in self.strategies:
            score = strategy.calculate_score(context)
            weighted_score = score * weight
            total_score += weighted_score

        return int(round(total_score))

    def get_strategy_name(self) -> str:
        """Retorna nome composto das estratégias"""
        strategy_names = [s.get_strategy_name() for s, _ in self.strategies]
        return f"composite({'+'.join(strategy_names)})"

    def get_breakdown(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Retorna breakdown detalhado de como pontuação foi calculada.

        Args:
            context: Contexto com todos os dados necessários

        Returns:
            Dicionário com detalhes de cada estratégia
        """
        breakdown = {
            'total_score': self.calculate_score(context),
            'components': []
        }

        for strategy, weight in self.strategies:
            score = strategy.calculate_score(context)
            weighted_score = score * weight

            breakdown['components'].append({
                'strategy': strategy.get_strategy_name(),
                'score': score,
                'weight': weight,
                'weighted_score': weighted_score
            })

        return breakdown
