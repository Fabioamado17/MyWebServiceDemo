"""
Módulo de Session Analytics - REFATORADO.

REFATORAÇÃO APLICADA: Blob/God Object → Componentes SRP

A classe monolítica original foi decomposta em 5 componentes:
1. SessionManager - Gestão de sessões
2. EventTracker - Registo de eventos
3. StatisticsCalculator - Cálculo de estatísticas
4. StreakManager - Gestão de streaks
5. AnalyticsExporter - Exportação para Inven!RA

Esta classe agora atua como FACADE, delegando para os componentes.

Autor: Fábio Amado (2501444@estudante.uab.pt)
"""
from typing import Dict, List, Optional, Any
from models.challenge import Challenge
from strategies.score_calculator import ScoreCalculator
from strategies.composite_scoring import CompositeScoringStrategy
from strategies.time_based_scoring import TimeBasedScoringStrategy
from strategies.accuracy_scoring import AccuracyScoringStrategy
from strategies.streak_scoring import StreakScoringStrategy

# Componentes SRP (Refatoração Blob/God Object)
from session_module.components.session_manager import SessionManager
from session_module.components.event_tracker import EventTracker
from session_module.components.statistics_calculator import StatisticsCalculator
from session_module.components.streak_manager import StreakManager
from session_module.components.analytics_exporter import AnalyticsExporter


class SessionAnalytics:
    """
    Facade para o Sistema de Analytics de Sessão.

    PADRÃO ESTRUTURAL: Facade
    - Fornece interface unificada para os componentes
    - Mantém compatibilidade com código existente
    - Delega operações para componentes especializados

    ANTIPADRÃO RESOLVIDO: Blob/God Object
    - Antes: 464 linhas, 6+ responsabilidades
    - Depois: ~150 linhas, apenas coordenação
    """

    def __init__(self):
        """Inicializa o sistema com componentes especializados."""
        # Componentes SRP
        self._session_manager = SessionManager()
        self._event_tracker = EventTracker()
        self._stats_calculator = StatisticsCalculator()
        self._streak_manager = StreakManager()
        self._analytics_exporter = AnalyticsExporter()

        # Strategy Pattern: Calculador de pontuação
        self.score_calculator = ScoreCalculator(
            CompositeScoringStrategy([
                (TimeBasedScoringStrategy(), 0.4),
                (AccuracyScoringStrategy(), 0.4),
                (StreakScoringStrategy(), 0.2)
            ])
        )

    # =========================================================
    # PROPRIEDADES (Backward Compatibility)
    # =========================================================

    @property
    def sessions(self) -> Dict[str, Dict]:
        """Acesso direto às sessões (backward compatibility)."""
        return self._session_manager.sessions

    @property
    def user_sessions(self) -> Dict[str, List[str]]:
        """Acesso direto às sessões por user (backward compatibility)."""
        return self._session_manager.user_sessions

    @property
    def user_stats(self) -> Dict[str, Dict]:
        """Acesso direto às stats (backward compatibility)."""
        return self._stats_calculator.user_stats

    # =========================================================
    # MÉTODOS PÚBLICOS (Facade)
    # =========================================================

    def start_session(self, user_id: str,
                     session_id: Optional[str] = None) -> str:
        """
        Inicia uma nova sessão de jogo.

        Args:
            user_id: ID do utilizador
            session_id: ID personalizado (opcional)

        Returns:
            ID da sessão criada
        """
        # Delegar para SessionManager
        session_id = self._session_manager.create_session(user_id, session_id)

        # Inicializar stats do utilizador se necessário
        self._stats_calculator.init_user_stats(user_id)
        self._stats_calculator.increment_session_count(user_id)

        # Atualizar dias consecutivos
        self._streak_manager.update_consecutive_days(
            self._stats_calculator.user_stats[user_id]
        )

        return session_id

    def log_challenge_start(self, session_id: str,
                           challenge: Challenge) -> None:
        """
        Regista início de um desafio.

        Args:
            session_id: ID da sessão
            challenge: Instância de Challenge
        """
        session = self._session_manager.get_session(session_id)

        # Delegar para EventTracker
        self._event_tracker.log_challenge_start(session, challenge)

        # Atualizar stats do utilizador
        user_id = session['user_id']
        self._stats_calculator.increment_challenge_count(user_id)
        self._stats_calculator.increment_interaction_count(user_id)

    def log_challenge_complete(self, session_id: str,
                              challenge_id: str,
                              is_correct: bool,
                              difficulty: int = 3,
                              time_limit: Optional[float] = None) -> Dict[str, Any]:
        """
        Regista conclusão de um desafio e calcula pontuação.

        Args:
            session_id: ID da sessão
            challenge_id: ID do desafio
            is_correct: Se resposta estava correta
            difficulty: Nível de dificuldade
            time_limit: Limite de tempo

        Returns:
            Resultado da pontuação
        """
        session = self._session_manager.get_session(session_id)
        user_id = session['user_id']

        # Incrementar tentativas
        attempts = self._event_tracker.increment_attempts(
            session, challenge_id
        )

        # Encontrar tempo do desafio
        start_interaction = self._event_tracker._find_challenge_start(
            session, challenge_id
        )

        duration = 0
        if start_interaction:
            from datetime import datetime
            duration = (
                datetime.now() - start_interaction['start_time']
            ).total_seconds()

        # Calcular pontuação usando Strategy Pattern
        scoring_context = {
            'time_taken': duration,
            'time_limit': time_limit or 30,
            'is_correct': is_correct,
            'attempts': attempts,
            'difficulty': difficulty,
            'streak': session['current_streak']
        }
        score_result = self.score_calculator.get_detailed_result(scoring_context)

        # Registar evento de conclusão
        self._event_tracker.log_challenge_complete(
            session, challenge_id, is_correct, score_result
        )

        # Atualizar streak na sessão
        current_streak = self._streak_manager.update_session_streak(
            session, is_correct
        )

        # Armazenar score na sessão
        session['scores'].append(score_result)
        session['total_score'] += score_result['score']

        # Atualizar stats do utilizador
        self._stats_calculator.increment_interaction_count(user_id)
        self._streak_manager.check_best_streak(
            self._stats_calculator.user_stats[user_id],
            current_streak
        )

        return score_result

    def log_interaction(self, session_id: str,
                       event_type: str,
                       event_data: Optional[Dict] = None) -> None:
        """
        Regista uma interação genérica.

        Args:
            session_id: ID da sessão
            event_type: Tipo de evento
            event_data: Dados adicionais
        """
        session = self._session_manager.get_session(session_id)

        # Delegar para EventTracker
        self._event_tracker.log_interaction(session, event_type, event_data)

        # Atualizar stats
        self._stats_calculator.increment_interaction_count(session['user_id'])

    def end_session(self, session_id: str) -> Dict:
        """
        Termina uma sessão e calcula estatísticas.

        Args:
            session_id: ID da sessão

        Returns:
            Sumário da sessão
        """
        # Delegar terminação
        session = self._session_manager.end_session(session_id)

        if not session['active']:  # Já estava inativa
            return self.get_session_summary(session_id)

        # Atualizar stats do utilizador
        user_id = session['user_id']
        self._stats_calculator.update_play_time(user_id, session['duration'])
        self._stats_calculator.update_score_stats(
            user_id,
            session['total_score'],
            session['current_streak']
        )

        return self.get_session_summary(session_id)

    def get_session_summary(self, session_id: str) -> Dict:
        """
        Retorna sumário de uma sessão.

        Args:
            session_id: ID da sessão

        Returns:
            Sumário completo
        """
        session = self._session_manager.get_session(session_id)
        return self._stats_calculator.calculate_session_summary(session)

    def get_user_sessions_report(self, user_id: str) -> Dict:
        """
        Retorna relatório de todas as sessões de um utilizador.

        Args:
            user_id: ID do utilizador

        Returns:
            Relatório agregado
        """
        session_ids = self._session_manager.get_user_sessions(user_id)
        sessions_data = [
            self.get_session_summary(sid) for sid in session_ids
        ]

        return self._stats_calculator.calculate_user_report(
            user_id, sessions_data
        )

    def export_analytics(self, user_id: str) -> Dict:
        """
        Exporta analytics em formato Inven!RA.

        Args:
            user_id: ID do utilizador

        Returns:
            Dados formatados para Inven!RA
        """
        user_stats = self._stats_calculator.user_stats.get(user_id)
        return self._analytics_exporter.export_for_invenira(user_id, user_stats)


# Instância global (singleton para simplificar)
session_analytics = SessionAnalytics()
