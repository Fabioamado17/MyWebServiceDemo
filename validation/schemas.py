"""
Schemas de Validação - Refatoração Input Kludge.

Este módulo define schemas de validação robustos que verificam:
- Presença de campos obrigatórios
- Tipos de dados corretos
- Formatos válidos
- Valores dentro de ranges permitidos
- Existência de recursos referenciados

ANTIPADRÃO RESOLVIDO: Input Kludge
- Antes: Validação apenas de presença (if 'field' in data)
- Depois: Validação completa de tipos, formatos e valores

Autor: Fábio Amado (2501444)
"""
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from enum import Enum


class ValidationError(Exception):
    """Exceção para erros de validação."""
    pass


class ChallengeType(Enum):
    """Tipos de desafio válidos."""
    AUDIO = 'audio'
    VISUAL = 'visual'
    HABITAT = 'habitat'
    CLASSIFICATION = 'classification'
    RANDOM = 'random'

    @classmethod
    def values(cls) -> List[str]:
        return [e.value for e in cls]


class EventType(Enum):
    """Tipos de evento/interação válidos."""
    CLICK_HINT = 'click_hint'
    CLICK_AUDIO = 'click_audio'
    HOVER_OPTION = 'hover_option'
    NAVIGATION = 'navigation'
    SUBMIT_ANSWER = 'submit_answer'
    CHALLENGE_START = 'challenge_start'
    CHALLENGE_COMPLETE = 'challenge_complete'


@dataclass
class SessionStartRequest:
    """
    Schema para iniciar sessão.

    Validações:
    - user_id: string não vazia, max 100 caracteres
    - session_id: opcional, string se fornecido
    """
    user_id: str
    session_id: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SessionStartRequest':
        """Cria instância a partir de dicionário."""
        return cls(
            user_id=data.get('user_id'),
            session_id=data.get('session_id')
        )

    def validate(self) -> None:
        """Valida todos os campos."""
        # Validar user_id
        if not self.user_id:
            raise ValueError("user_id é obrigatório")

        if not isinstance(self.user_id, str):
            raise ValueError("user_id deve ser uma string")

        if len(self.user_id.strip()) == 0:
            raise ValueError("user_id não pode ser vazio")

        if len(self.user_id) > 100:
            raise ValueError("user_id muito longo (máximo 100 caracteres)")

        # Validar session_id (se fornecido)
        if self.session_id is not None:
            if not isinstance(self.session_id, str):
                raise ValueError("session_id deve ser uma string")

            if len(self.session_id) > 200:
                raise ValueError("session_id muito longo (máximo 200 caracteres)")


@dataclass
class ChallengeRequest:
    """
    Schema para criar desafio em sessão.

    Validações:
    - session_id: string, sessão deve existir e estar ativa
    - animal_id: inteiro positivo, animal deve existir
    - challenge_type: deve ser tipo válido
    - difficulty: inteiro entre 1 e 5
    """
    session_id: str
    animal_id: int
    challenge_type: str = 'random'
    difficulty: int = 1

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ChallengeRequest':
        """Cria instância a partir de dicionário."""
        return cls(
            session_id=data.get('session_id'),
            animal_id=data.get('animal_id'),
            challenge_type=data.get('challenge_type', 'random'),
            difficulty=data.get('difficulty', 1)
        )

    def validate(self) -> None:
        """Valida todos os campos."""
        # Validar session_id
        if not self.session_id:
            raise ValueError("session_id é obrigatório")

        if not isinstance(self.session_id, str):
            raise ValueError("session_id deve ser uma string")

        # Validar animal_id
        if self.animal_id is None:
            raise ValueError("animal_id é obrigatório")

        if not isinstance(self.animal_id, int):
            raise ValueError("animal_id deve ser um número inteiro")

        if self.animal_id < 1:
            raise ValueError("animal_id deve ser um número positivo")

        # Validar se animal existe
        from data.animals_data import ANIMALS_DB
        if not any(a['id'] == self.animal_id for a in ANIMALS_DB):
            raise ValueError(f"Animal com ID {self.animal_id} não existe")

        # Validar challenge_type
        if self.challenge_type not in ChallengeType.values():
            raise ValueError(
                f"challenge_type '{self.challenge_type}' inválido. "
                f"Tipos válidos: {ChallengeType.values()}"
            )

        # Validar difficulty
        if not isinstance(self.difficulty, int):
            raise ValueError("difficulty deve ser um número inteiro")

        if not 1 <= self.difficulty <= 5:
            raise ValueError("difficulty deve estar entre 1 e 5")

    def validate_session_exists(self, session_analytics) -> None:
        """Valida se a sessão existe e está ativa."""
        if self.session_id not in session_analytics.sessions:
            raise ValueError(f"Sessão '{self.session_id}' não existe")

        if not session_analytics.sessions[self.session_id]['active']:
            raise ValueError(f"Sessão '{self.session_id}' já foi encerrada")


@dataclass
class ChallengeCompleteRequest:
    """
    Schema para concluir desafio.

    Validações:
    - session_id: string, sessão deve existir
    - challenge_id: string, desafio deve ter sido iniciado na sessão
    - is_correct: deve ser booleano
    - difficulty: opcional, inteiro 1-5
    - time_limit: opcional, número positivo
    """
    session_id: str
    challenge_id: str
    is_correct: bool
    difficulty: int = 3
    time_limit: Optional[float] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ChallengeCompleteRequest':
        """Cria instância a partir de dicionário."""
        return cls(
            session_id=data.get('session_id'),
            challenge_id=data.get('challenge_id'),
            is_correct=data.get('is_correct'),
            difficulty=data.get('difficulty', 3),
            time_limit=data.get('time_limit')
        )

    def validate(self) -> None:
        """Valida todos os campos."""
        # Validar session_id
        if not self.session_id:
            raise ValueError("session_id é obrigatório")

        if not isinstance(self.session_id, str):
            raise ValueError("session_id deve ser uma string")

        # Validar challenge_id
        if not self.challenge_id:
            raise ValueError("challenge_id é obrigatório")

        if not isinstance(self.challenge_id, str):
            raise ValueError("challenge_id deve ser uma string")

        # Validar is_correct - IMPORTANTE: deve ser booleano, não string
        if self.is_correct is None:
            raise ValueError("is_correct é obrigatório")

        if not isinstance(self.is_correct, bool):
            raise ValueError(
                "is_correct deve ser um booleano (true/false), "
                f"recebido: {type(self.is_correct).__name__}"
            )

        # Validar difficulty
        if not isinstance(self.difficulty, int):
            raise ValueError("difficulty deve ser um número inteiro")

        if not 1 <= self.difficulty <= 5:
            raise ValueError("difficulty deve estar entre 1 e 5")

        # Validar time_limit (se fornecido)
        if self.time_limit is not None:
            if not isinstance(self.time_limit, (int, float)):
                raise ValueError("time_limit deve ser um número")

            if self.time_limit <= 0:
                raise ValueError("time_limit deve ser positivo")

    def validate_challenge_started(self, session_analytics) -> None:
        """Valida se o desafio foi iniciado na sessão."""
        if self.session_id not in session_analytics.sessions:
            raise ValueError(f"Sessão '{self.session_id}' não existe")

        session = session_analytics.sessions[self.session_id]
        challenge_started = any(
            i['type'] == 'challenge_start' and
            i['challenge_id'] == self.challenge_id
            for i in session['interactions']
        )

        if not challenge_started:
            raise ValueError(
                f"Desafio '{self.challenge_id}' não foi iniciado nesta sessão"
            )


@dataclass
class InteractionRequest:
    """
    Schema para registar interação.

    Validações:
    - session_id: string, sessão deve existir
    - event_type: string não vazia
    - event_data: opcional, dicionário
    """
    session_id: str
    event_type: str
    event_data: Optional[Dict[str, Any]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'InteractionRequest':
        """Cria instância a partir de dicionário."""
        return cls(
            session_id=data.get('session_id'),
            event_type=data.get('event_type'),
            event_data=data.get('event_data')
        )

    def validate(self) -> None:
        """Valida todos os campos."""
        # Validar session_id
        if not self.session_id:
            raise ValueError("session_id é obrigatório")

        if not isinstance(self.session_id, str):
            raise ValueError("session_id deve ser uma string")

        # Validar event_type
        if not self.event_type:
            raise ValueError("event_type é obrigatório")

        if not isinstance(self.event_type, str):
            raise ValueError("event_type deve ser uma string")

        if len(self.event_type.strip()) == 0:
            raise ValueError("event_type não pode ser vazio")

        # Validar event_data (se fornecido)
        if self.event_data is not None:
            if not isinstance(self.event_data, dict):
                raise ValueError("event_data deve ser um objeto/dicionário")


@dataclass
class SessionEndRequest:
    """
    Schema para terminar sessão.

    Validações:
    - session_id: string, sessão deve existir
    """
    session_id: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SessionEndRequest':
        """Cria instância a partir de dicionário."""
        return cls(session_id=data.get('session_id'))

    def validate(self) -> None:
        """Valida todos os campos."""
        if not self.session_id:
            raise ValueError("session_id é obrigatório")

        if not isinstance(self.session_id, str):
            raise ValueError("session_id deve ser uma string")


@dataclass
class AnalyticsRequest:
    """
    Schema para obter analytics (compatível Inven!RA).

    Validações:
    - studentId: string não vazia
    """
    student_id: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AnalyticsRequest':
        """Cria instância a partir de dicionário."""
        return cls(student_id=data.get('studentId'))

    def validate(self) -> None:
        """Valida todos os campos."""
        if not self.student_id:
            raise ValueError("studentId é obrigatório")

        if not isinstance(self.student_id, str):
            raise ValueError("studentId deve ser uma string")

        if len(self.student_id.strip()) == 0:
            raise ValueError("studentId não pode ser vazio")
