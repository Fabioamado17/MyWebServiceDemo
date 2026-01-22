"""
Módulo de Decorators para Desafios.

Padrão Estrutural: Decorator
Permite adicionar funcionalidades aos desafios de forma dinâmica e composível.

Este módulo implementa o padrão Decorator para adicionar comportamentos
adicionais aos desafios do jogo "Dia & Noite" sem modificar as classes base.

Classes Disponíveis:
------------------
- ChallengeDecorator: Decorator base abstrato
- TimedDecorator: Adiciona limite de tempo aos desafios

Example:
-------
>>> from factories.challenge_factory import ChallengeFactory
>>> from decorators import TimedDecorator
>>>
>>> # Criar e decorar desafio
>>> challenge = ChallengeFactory.create_challenge('audio', animal_id=1)
>>> timed_challenge = TimedDecorator(challenge, time_limit=30)
>>>
>>> # Usar normalmente
>>> timed_challenge.start_timer()
>>> question = timed_challenge.get_question()
>>> # ...
>>> is_correct = timed_challenge.validate_answer(answer)

Autor: Fábio Amado (2501444)
UC: Arquitetura e Padrões de Software
Universidade Aberta
"""

from decorators.challenge_decorator import ChallengeDecorator
from decorators.timed_decorator import TimedDecorator

__all__ = [
    'ChallengeDecorator',
    'TimedDecorator'
]

__version__ = '1.0.0'
