"""
Score Calculator - Context for Strategy Pattern

Contexto que usa as estratégias de pontuação.
Permite trocar estratégias em runtime.

Autor: Fábio Amado (2501444@estudante.uab.pt)
"""
from typing import Dict, Any, Optional
from strategies.scoring_strategy import ScoringStrategy
from strategies.time_based_scoring import TimeBasedScoringStrategy


class ScoreCalculator:
    """
    Context: Calculador de Pontuação.

    Usa Strategy Pattern para permitir diferentes algoritmos
    de pontuação sem modificar o código cliente.

    Exemplo de uso:
        calculator = ScoreCalculator()
        calculator.set_strategy(TimeBasedScoringStrategy())
        score = calculator.calculate(context)
    """

    def __init__(self, strategy: Optional[ScoringStrategy] = None):
        """
        Inicializa o calculador com uma estratégia.

        Args:
            strategy: Estratégia inicial (default: TimeBasedScoringStrategy)
        """
        self._strategy = strategy or TimeBasedScoringStrategy()

    def set_strategy(self, strategy: ScoringStrategy) -> None:
        """
        Altera a estratégia de pontuação em runtime.

        Demonstra o poder do Strategy Pattern:
        - Trocar comportamento sem recompilar
        - Código cliente não precisa mudar

        Args:
            strategy: Nova estratégia a usar
        """
        self._strategy = strategy

    def get_strategy(self) -> ScoringStrategy:
        """
        Retorna a estratégia atual.

        Returns:
            Estratégia de pontuação em uso
        """
        return self._strategy

    def calculate(self, context: Dict[str, Any]) -> int:
        """
        Calcula pontuação usando a estratégia atual.

        Args:
            context: Contexto com dados do desafio:
                - time_taken: Tempo gasto (segundos)
                - time_limit: Limite de tempo (segundos)
                - is_correct: Se resposta estava correta
                - attempts: Número de tentativas
                - difficulty: Nível de dificuldade (1-5)
                - streak: Sequência de acertos consecutivos

        Returns:
            Pontuação calculada (0-100)
        """
        return self._strategy.calculate_score(context)

    def get_performance_level(self, context: Dict[str, Any]) -> str:
        """
        Calcula e retorna nível de performance.

        Args:
            context: Contexto com dados do desafio

        Returns:
            Nível de performance (excellent, good, fair, poor)
        """
        score = self.calculate(context)
        return self._strategy.get_performance_level(score)

    def get_detailed_result(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Retorna resultado detalhado com metadados.

        Args:
            context: Contexto com dados do desafio

        Returns:
            Dicionário com score, strategy, performance, etc.
        """
        score = self.calculate(context)
        performance = self._strategy.get_performance_level(score)

        result = {
            'score': score,
            'performance': performance,
            'strategy': self._strategy.get_strategy_name(),
            'context': context
        }

        # Se for CompositeScoringStrategy, adicionar breakdown
        if hasattr(self._strategy, 'get_breakdown'):
            result['breakdown'] = self._strategy.get_breakdown(context)

        return result
