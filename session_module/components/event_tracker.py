"""
Rastreador de Eventos - Componente SRP.

Responsabilidade Única: Registar eventos (desafios, interações).

Autor: Fábio Amado (2501444)
"""
from typing import Dict, Optional, Any
from datetime import datetime
from models.challenge import Challenge


class EventTracker:
    """
    Regista eventos de desafios e interações.

    Responsabilidades:
    - Registar início de desafios
    - Registar conclusão de desafios
    - Registar interações genéricas
    - Calcular tempo por desafio
    """

    def log_challenge_start(self, session: Dict,
                           challenge: Challenge) -> None:
        """
        Regista início de um desafio.

        Args:
            session: Dados da sessão (modificado in-place)
            challenge: Instância do desafio
        """
        interaction = {
            'type': 'challenge_start',
            'challenge_id': challenge.challenge_id,
            'challenge_type': challenge.get_challenge_type(),
            'animal_id': challenge.animal_id,
            'timestamp': datetime.now().isoformat(),
            'start_time': datetime.now()
        }

        session['interactions'].append(interaction)
        session['challenges_attempted'] += 1

        # Inicializar tracking de tentativas
        if challenge.challenge_id not in session['current_challenge_attempts']:
            session['current_challenge_attempts'][challenge.challenge_id] = 0

    def log_challenge_complete(self, session: Dict,
                              challenge_id: str,
                              is_correct: bool,
                              score_result: Dict) -> float:
        """
        Regista conclusão de um desafio.

        Args:
            session: Dados da sessão (modificado in-place)
            challenge_id: ID do desafio
            is_correct: Se resposta estava correta
            score_result: Resultado do cálculo de pontuação

        Returns:
            Duração do desafio em segundos
        """
        # Encontrar interação de início
        start_interaction = self._find_challenge_start(
            session, challenge_id
        )

        duration = 0
        if start_interaction:
            end_time = datetime.now()
            duration = (end_time - start_interaction['start_time']).total_seconds()

            session['challenge_times'].append({
                'challenge_id': challenge_id,
                'challenge_type': start_interaction['challenge_type'],
                'duration': duration,
                'is_correct': is_correct,
                'attempts': session['current_challenge_attempts'].get(
                    challenge_id, 1
                ),
                'score': score_result.get('score', 0),
                'performance': score_result.get('performance', 'poor')
            })

        # Registar interação de conclusão
        interaction = {
            'type': 'challenge_complete',
            'challenge_id': challenge_id,
            'is_correct': is_correct,
            'timestamp': datetime.now().isoformat(),
            'score': score_result.get('score', 0),
            'performance': score_result.get('performance', 'poor')
        }
        session['interactions'].append(interaction)

        return duration

    def log_interaction(self, session: Dict,
                       event_type: str,
                       event_data: Optional[Dict] = None) -> None:
        """
        Regista uma interação genérica.

        Args:
            session: Dados da sessão (modificado in-place)
            event_type: Tipo do evento
            event_data: Dados adicionais
        """
        interaction = {
            'type': event_type,
            'timestamp': datetime.now().isoformat(),
            'data': event_data or {}
        }
        session['interactions'].append(interaction)

    def increment_attempts(self, session: Dict, challenge_id: str) -> int:
        """
        Incrementa contador de tentativas para um desafio.

        Returns:
            Número de tentativas atual
        """
        attempts = session['current_challenge_attempts'].get(challenge_id, 0) + 1
        session['current_challenge_attempts'][challenge_id] = attempts
        return attempts

    def _find_challenge_start(self, session: Dict,
                             challenge_id: str) -> Optional[Dict]:
        """Encontra interação de início de um desafio."""
        for interaction in reversed(session['interactions']):
            if (interaction['type'] == 'challenge_start' and
                interaction['challenge_id'] == challenge_id):
                return interaction
        return None
