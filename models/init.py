"""
Módulo de modelos do jogo Dia & Noite.
Contém as classes de desafios implementando o padrão Factory Method.

Autores: Henrique Crachat (2501450) & Fábio Amado (2501444)
UC: Arquitetura e Padrões de Software
"""

from models.challenge import Challenge
from models.audio_challenge import AudioChallenge
from models.visual_challenge import VisualChallenge
from models.habitat_challenge import HabitatChallenge
from models.classification_challenge import ClassificationChallenge

__all__ = [
    'Challenge',
    'AudioChallenge',
    'VisualChallenge',
    'HabitatChallenge',
    'ClassificationChallenge'
]

__version__ = '1.0.0'
__author__ = 'Henrique Crachat & Fábio Amado'
