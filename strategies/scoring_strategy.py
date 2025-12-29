"""
Padrão Strategy para Sistema de Pontuação - Fábio Amado (2501444)

Strategy Pattern (Behavioral):
- Permite definir uma família de algoritmos de pontuação
- Encapsula cada algoritmo de forma independente
- Torna-os intercambiáveis sem alterar o cliente

Autor: Fábio Amado (2501444@estudante.uab.pt)
"""
from abc import ABC, abstractmethod
from typing import Dict, Any


class ScoringStrategy(ABC):
    """
    Interface Strategy para cálculo de pontuação.

    Define o contrato que todas as estratégias concretas
    devem implementar. Permite trocar algoritmos de pontuação
    em runtime sem modificar o código cliente.
    """

    @abstractmethod
    def calculate_score(self, context: Dict[str, Any]) -> int:
        """
        Calcula pontuação baseado no contexto fornecido.

        Args:
            context: Dicionário com dados relevantes para cálculo:
                - time_taken: Tempo gasto (segundos)
                - time_limit: Limite de tempo (segundos)
                - is_correct: Se resposta estava correta
                - attempts: Número de tentativas
                - difficulty: Nível de dificuldade (1-5)
                - streak: Sequência de acertos consecutivos
                - etc.

        Returns:
            Pontuação calculada (0-100)
        """
        pass

    @abstractmethod
    def get_strategy_name(self) -> str:
        """
        Retorna o nome da estratégia.

        Returns:
            Nome identificador da estratégia
        """
        pass

    def get_performance_level(self, score: int) -> str:
        """
        Converte pontuação em nível de performance.

        Args:
            score: Pontuação (0-100)

        Returns:
            Nível de performance (excellent, good, fair, poor)
        """
        if score >= 90:
            return 'excellent'
        elif score >= 70:
            return 'good'
        elif score >= 50:
            return 'fair'
        else:
            return 'poor'
