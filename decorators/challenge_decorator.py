"""
Decorator base para desafios.

Padrão Estrutural: Decorator
Este é o Decorator abstrato que mantém referência ao componente decorado.

Autores: Henrique Crachat (2501450) & Fábio Amado (2501444)
UC: Arquitetura e Padrões de Software
Universidade Aberta
"""
from abc import ABC
from models.challenge import Challenge
from typing import List, Dict, Any


class ChallengeDecorator(Challenge, ABC):
    """
    Classe base abstrata para decoradores de desafios.

    PADRÃO ESTRUTURAL: Decorator

    Propósito:
    --------
    Permite adicionar funcionalidades a objetos Challenge existentes de forma
    dinâmica, sem modificar a estrutura das classes base. O decorator mantém
    uma referência ao Challenge decorado e delega chamadas a ele, podendo
    adicionar comportamento antes ou depois.

    Problema Resolvido:
    -----------------
    No jogo "Dia & Noite", diferentes desafios podem precisar de funcionalidades
    adicionais (tempo limite, dicas, pontuação extra, etc.). Criar subclasses
    para todas as combinações seria impraticável (AudioTimedChallenge,
    AudioTimedScoredChallenge, etc.).

    Solução:
    -------
    O padrão Decorator permite "embrulhar" um desafio básico com funcionalidades
    adicionais de forma modular e composível. Cada decorator adiciona uma
    funcionalidade específica e pode ser combinado com outros decorators.

    Vantagens:
    ---------
    1. Flexibilidade: Adicionar/remover funcionalidades em runtime
    2. Composição: Combinar múltiplos decorators
    3. Open/Closed: Estender funcionalidade sem modificar classes base
    4. Single Responsibility: Cada decorator tem uma responsabilidade
    5. Reutilização: Decorators podem ser aplicados a qualquer Challenge

    Participantes do Padrão:
    ----------------------
    - Component (Challenge): Interface base
    - ConcreteComponent: AudioChallenge, VisualChallenge, etc.
    - Decorator (ChallengeDecorator): Esta classe base
    - ConcreteDecorator: TimedDecorator, HintDecorator, etc.

    Example:
    -------
    >>> # Criar challenge básico
    >>> base_challenge = ChallengeFactory.create_challenge('audio', animal_id=1)
    >>>
    >>> # Decorar com funcionalidade de tempo
    >>> timed_challenge = TimedDecorator(base_challenge, time_limit=30)
    >>>
    >>> # Interface permanece igual
    >>> question = timed_challenge.get_question()
    >>>
    >>> # Mas agora tem funcionalidades adicionais
    >>> time_left = timed_challenge.get_time_remaining()
    """

    def __init__(self, challenge: Challenge):
        """
        Inicializa o decorator com um desafio a decorar.

        Args:
            challenge: Desafio a ser decorado (pode ser um desafio básico
                      ou já decorado por outros decorators)
        """
        # Não chamar super().__init__() porque não queremos criar um novo desafio
        # Apenas manter referência ao desafio decorado
        self._challenge = challenge

        # Copiar atributos básicos do desafio decorado
        self.animal_id = challenge.animal_id
        self.difficulty = challenge.difficulty
        self.challenge_id = challenge.challenge_id
        self.correct_answer = challenge.correct_answer

    def get_question(self) -> str:
        """
        Delega a obtenção da pergunta ao desafio decorado.

        Returns:
            Pergunta do desafio
        """
        return self._challenge.get_question()

    def get_options(self) -> List[str]:
        """
        Delega a obtenção das opções ao desafio decorado.

        Returns:
            Lista de opções de resposta
        """
        return self._challenge.get_options()

    def get_challenge_type(self) -> str:
        """
        Delega a obtenção do tipo ao desafio decorado.

        Returns:
            Tipo do desafio ('audio', 'visual', etc.)
        """
        return self._challenge.get_challenge_type()

    def validate_answer(self, answer: str) -> bool:
        """
        Delega a validação da resposta ao desafio decorado.

        Args:
            answer: Resposta fornecida pelo aluno

        Returns:
            True se a resposta está correta
        """
        return self._challenge.validate_answer(answer)

    def to_dict(self) -> Dict[str, Any]:
        """
        Delega a conversão para dicionário ao desafio decorado.

        Decorators concretos podem sobrescrever este método para
        adicionar informações extras ao dicionário.

        Returns:
            Dicionário com dados do desafio
        """
        return self._challenge.to_dict()

    def get_decorated_challenge(self) -> Challenge:
        """
        Retorna o desafio decorado (útil para aceder ao desafio original).

        Returns:
            Desafio que está sendo decorado
        """
        return self._challenge

    def __repr__(self) -> str:
        """Representação em string do decorator"""
        return f"{self.__class__.__name__}({self._challenge})"
