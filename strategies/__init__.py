"""
Strategies Module - Strategy Pattern Implementation

Padrão Strategy (Behavioral) para Sistema de Pontuação.

Autor: Fábio Amado (2501444@estudante.uab.pt)
"""
from strategies.scoring_strategy import ScoringStrategy
from strategies.time_based_scoring import TimeBasedScoringStrategy
from strategies.accuracy_scoring import AccuracyScoringStrategy
from strategies.streak_scoring import StreakScoringStrategy
from strategies.difficulty_scoring import DifficultyBasedScoringStrategy
from strategies.composite_scoring import CompositeScoringStrategy

__all__ = [
    'ScoringStrategy',
    'TimeBasedScoringStrategy',
    'AccuracyScoringStrategy',
    'StreakScoringStrategy',
    'DifficultyBasedScoringStrategy',
    'CompositeScoringStrategy'
]
