"""
Módulo de Session Analytics - Fábio Amado (2501444)

Integração do padrão Factory Method com tracking de sessões.
Responsável por monitorizar:
- Tempo de jogo por sessão
- Número de sessões
- Interações por desafio
- Dias consecutivos de jogo
- Padrões de uso
- Pontuação com Strategy Pattern (Atividade 6)

Autor: Fábio Amado (2501444@estudante.uab.pt)
"""
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from models.challenge import Challenge
from strategies.score_calculator import ScoreCalculator
from strategies.composite_scoring import CompositeScoringStrategy
from strategies.time_based_scoring import TimeBasedScoringStrategy
from strategies.accuracy_scoring import AccuracyScoringStrategy
from strategies.streak_scoring import StreakScoringStrategy


class SessionAnalytics:
    """
    Sistema de Analytics de Sessão.
    
    Usa o Factory Method (ChallengeFactory) para obter desafios
    e monitoriza padrões de sessão e interação do aluno.
    """
    
    def __init__(self):
        """Inicializa o sistema de session analytics"""
        # Estrutura: {session_id: {dados}}
        self.sessions: Dict[str, Dict] = {}
        # Estrutura: {user_id: [session_ids]}
        self.user_sessions: Dict[str, List[str]] = {}
        # Estrutura: {user_id: {estatísticas}}
        self.user_stats: Dict[str, Dict] = {}

        # Strategy Pattern: Calculador de pontuação (Atividade 6)
        # Usa estratégia composta por default (tempo + precisão + streak)
        self.score_calculator = ScoreCalculator(
            CompositeScoringStrategy([
                (TimeBasedScoringStrategy(), 0.4),    # 40% peso para tempo
                (AccuracyScoringStrategy(), 0.4),     # 40% peso para precisão
                (StreakScoringStrategy(), 0.2)        # 20% peso para streak
            ])
        )
    
    def start_session(self, user_id: str, session_id: Optional[str] = None) -> str:
        """
        Inicia uma nova sessão de jogo.
        
        Args:
            user_id: ID do utilizador
            session_id: ID da sessão (gerado se None)
        
        Returns:
            ID da sessão criada
        """
        if session_id is None:
            session_id = f"{user_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Criar sessão
        self.sessions[session_id] = {
            'session_id': session_id,
            'user_id': user_id,
            'start_time': datetime.now().isoformat(),
            'end_time': None,
            'duration': 0,
            'challenges_attempted': 0,
            'interactions': [],
            'challenge_times': [],  # Tempo por desafio
            'active': True,
            # Campos para Strategy Pattern (Atividade 6)
            'current_streak': 0,         # Streak atual de acertos
            'current_challenge_attempts': {},  # {challenge_id: attempts}
            'scores': [],                # Pontuações de cada desafio
            'total_score': 0             # Pontuação total da sessão
        }
        
        # Registar sessão do utilizador
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = []
            self.user_stats[user_id] = {
                'total_sessions': 0,
                'total_play_time': 0,
                'total_challenges': 0,
                'total_interactions': 0,
                'consecutive_days': 0,
                'last_play_date': None,
                'play_dates': [],
                # Campos para Strategy Pattern (Atividade 6)
                'total_score': 0,            # Pontuação total acumulada
                'best_streak': 0,            # Melhor streak de todos os tempos
                'avg_score': 0.0             # Pontuação média
            }
        
        self.user_sessions[user_id].append(session_id)
        self.user_stats[user_id]['total_sessions'] += 1
        
        # Atualizar dias consecutivos
        self._update_consecutive_days(user_id)
        
        return session_id
    
    def log_challenge_start(self, session_id: str, challenge: Challenge) -> None:
        """
        Regista início de um desafio.
        
        Integração com Factory Method:
        - Recebe instância de Challenge criada pelo Factory
        - Extrai informações do desafio para tracking
        
        Args:
            session_id: ID da sessão
            challenge: Instância de Challenge (do Factory)
        """
        if session_id not in self.sessions:
            raise ValueError(f"Sessão {session_id} não encontrada")
        
        session = self.sessions[session_id]
        
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

        # Inicializar tracking de tentativas para este desafio (Atividade 6)
        if challenge.challenge_id not in session['current_challenge_attempts']:
            session['current_challenge_attempts'][challenge.challenge_id] = 0

        # Atualizar stats do utilizador
        user_id = session['user_id']
        self.user_stats[user_id]['total_challenges'] += 1
        self.user_stats[user_id]['total_interactions'] += 1
    
    def log_challenge_complete(self, session_id: str, challenge_id: str,
                              is_correct: bool, difficulty: int = 3,
                              time_limit: Optional[float] = None) -> Dict[str, Any]:
        """
        Regista conclusão de um desafio e calcula pontuação (Strategy Pattern).

        Args:
            session_id: ID da sessão
            challenge_id: ID do desafio
            is_correct: Se a resposta estava correta
            difficulty: Nível de dificuldade (1-5, default: 3)
            time_limit: Limite de tempo em segundos (opcional)

        Returns:
            Dicionário com pontuação e detalhes calculados
        """
        if session_id not in self.sessions:
            raise ValueError(f"Sessão {session_id} não encontrada")
        
        session = self.sessions[session_id]
        
        # Encontrar interação de início correspondente
        start_interaction = None
        for interaction in reversed(session['interactions']):
            if (interaction['type'] == 'challenge_start' and 
                interaction['challenge_id'] == challenge_id):
                start_interaction = interaction
                break
        
        # Incrementar tentativas (Atividade 6)
        attempts = session['current_challenge_attempts'].get(challenge_id, 0) + 1
        session['current_challenge_attempts'][challenge_id] = attempts

        # Calcular tempo e pontuação (Strategy Pattern - Atividade 6)
        duration = 0
        score_result = {}

        if start_interaction:
            # Calcular tempo gasto no desafio
            end_time = datetime.now()
            duration = (end_time - start_interaction['start_time']).total_seconds()

            # Preparar contexto para Strategy Pattern
            scoring_context = {
                'time_taken': duration,
                'time_limit': time_limit or 30,  # Default 30s
                'is_correct': is_correct,
                'attempts': attempts,
                'difficulty': difficulty,
                'streak': session['current_streak']
            }

            # Calcular pontuação usando Strategy Pattern
            score_result = self.score_calculator.get_detailed_result(scoring_context)

            # Atualizar streak
            if is_correct:
                session['current_streak'] += 1
            else:
                session['current_streak'] = 0

            # Armazenar score
            session['scores'].append(score_result)
            session['total_score'] += score_result['score']

            session['challenge_times'].append({
                'challenge_id': challenge_id,
                'challenge_type': start_interaction['challenge_type'],
                'duration': duration,
                'is_correct': is_correct,
                'attempts': attempts,
                'score': score_result['score'],
                'performance': score_result['performance']
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

        # Atualizar stats do utilizador
        user_id = session['user_id']
        self.user_stats[user_id]['total_interactions'] += 1

        # Atualizar best streak (Atividade 6)
        if session['current_streak'] > self.user_stats[user_id]['best_streak']:
            self.user_stats[user_id]['best_streak'] = session['current_streak']

        return score_result
    
    def log_interaction(self, session_id: str, event_type: str, 
                       event_data: Optional[Dict] = None) -> None:
        """
        Regista uma interação genérica.
        
        Args:
            session_id: ID da sessão
            event_type: Tipo de evento (click, hover, navigation, etc)
            event_data: Dados adicionais do evento
        """
        if session_id not in self.sessions:
            raise ValueError(f"Sessão {session_id} não encontrada")
        
        session = self.sessions[session_id]
        
        interaction = {
            'type': event_type,
            'timestamp': datetime.now().isoformat(),
            'data': event_data or {}
        }
        
        session['interactions'].append(interaction)
        self.user_stats[session['user_id']]['total_interactions'] += 1
    
    def end_session(self, session_id: str) -> Dict:
        """
        Termina uma sessão e calcula estatísticas.
        
        Args:
            session_id: ID da sessão
        
        Returns:
            Sumário da sessão
        """
        if session_id not in self.sessions:
            raise ValueError(f"Sessão {session_id} não encontrada")
        
        session = self.sessions[session_id]
        
        if not session['active']:
            return self.get_session_summary(session_id)
        
        # Calcular duração
        start = datetime.fromisoformat(session['start_time'])
        end = datetime.now()
        duration = (end - start).total_seconds()
        
        session['end_time'] = end.isoformat()
        session['duration'] = duration
        session['active'] = False
        
        # Atualizar stats do utilizador (incluindo pontuação - Atividade 6)
        user_id = session['user_id']
        self.user_stats[user_id]['total_play_time'] += duration
        self.user_stats[user_id]['total_score'] += session['total_score']

        # Calcular média de pontuação
        total_challenges = self.user_stats[user_id]['total_challenges']
        if total_challenges > 0:
            self.user_stats[user_id]['avg_score'] = (
                self.user_stats[user_id]['total_score'] / total_challenges
            )

        return self.get_session_summary(session_id)
    
    def get_session_summary(self, session_id: str) -> Dict:
        """
        Retorna sumário de uma sessão.
        
        Args:
            session_id: ID da sessão
        
        Returns:
            Sumário completo da sessão
        """
        if session_id not in self.sessions:
            raise ValueError(f"Sessão {session_id} não encontrada")
        
        session = self.sessions[session_id]
        
        # Calcular tempo médio por desafio
        avg_challenge_time = 0
        if session['challenge_times']:
            avg_challenge_time = sum(
                ct['duration'] for ct in session['challenge_times']
            ) / len(session['challenge_times'])
        
        # Contar interações por tipo
        interaction_counts = {}
        for interaction in session['interactions']:
            itype = interaction['type']
            interaction_counts[itype] = interaction_counts.get(itype, 0) + 1
        
        return {
            'session_id': session_id,
            'user_id': session['user_id'],
            'duration': session['duration'],
            'challenges_attempted': session['challenges_attempted'],
            'total_interactions': len(session['interactions']),
            'interaction_breakdown': interaction_counts,
            'avg_challenge_time': round(avg_challenge_time, 2),
            'challenge_times': session['challenge_times'],
            'start_time': session['start_time'],
            'end_time': session['end_time'],
            'active': session['active'],
            # Dados de pontuação - Strategy Pattern (Atividade 6)
            'total_score': session.get('total_score', 0),
            'current_streak': session.get('current_streak', 0),
            'scores': session.get('scores', [])
        }
    
    def get_user_sessions_report(self, user_id: str) -> Dict:
        """
        Retorna relatório de todas as sessões de um utilizador.
        
        Args:
            user_id: ID do utilizador
        
        Returns:
            Relatório agregado de sessões
        """
        if user_id not in self.user_sessions:
            return {
                'user_id': user_id,
                'total_sessions': 0,
                'sessions': []
            }
        
        sessions_data = []
        for session_id in self.user_sessions[user_id]:
            sessions_data.append(self.get_session_summary(session_id))
        
        stats = self.user_stats[user_id]
        
        return {
            'user_id': user_id,
            'total_sessions': stats['total_sessions'],
            'total_play_time': stats['total_play_time'],
            'avg_session_time': (
                stats['total_play_time'] / stats['total_sessions']
                if stats['total_sessions'] > 0 else 0
            ),
            'total_challenges': stats['total_challenges'],
            'total_interactions': stats['total_interactions'],
            'consecutive_days': stats['consecutive_days'],
            # Dados de pontuação - Strategy Pattern (Atividade 6)
            'total_score': stats.get('total_score', 0),
            'avg_score': round(stats.get('avg_score', 0.0), 2),
            'best_streak': stats.get('best_streak', 0),
            'sessions': sessions_data
        }
    
    def _update_consecutive_days(self, user_id: str) -> None:
        """Atualiza contagem de dias consecutivos"""
        stats = self.user_stats[user_id]
        today = datetime.now().date()
        
        # Adicionar data de hoje
        if today not in stats['play_dates']:
            stats['play_dates'].append(today)
        
        # Calcular dias consecutivos
        if stats['last_play_date']:
            last_date = datetime.fromisoformat(stats['last_play_date']).date()
            diff = (today - last_date).days
            
            if diff == 1:
                # Dia consecutivo
                stats['consecutive_days'] += 1
            elif diff > 1:
                # Quebrou sequência
                stats['consecutive_days'] = 1
        else:
            stats['consecutive_days'] = 1
        
        stats['last_play_date'] = today.isoformat()
    
    def export_analytics(self, user_id: str) -> Dict:
        """
        Exporta analytics em formato compatível com Inven!RA.
        
        Args:
            user_id: ID do utilizador
        
        Returns:
            Dados formatados para Inven!RA
        """
        if user_id not in self.user_stats:
            return {
                'studentId': user_id,
                'activityId': 'dia-noite-animals',
                'sessionMetrics': {},
                'timestamp': datetime.now().isoformat()
            }
        
        stats = self.user_stats[user_id]
        
        return {
            'studentId': user_id,
            'activityId': 'dia-noite-animals',
            'sessionMetrics': {
                'totalSessions': stats['total_sessions'],
                'totalPlayTime': stats['total_play_time'],
                'totalChallenges': stats['total_challenges'],
                'totalInteractions': stats['total_interactions'],
                'consecutiveDays': stats['consecutive_days'],
                'avgSessionTime': (
                    stats['total_play_time'] / stats['total_sessions']
                    if stats['total_sessions'] > 0 else 0
                ),
                # Dados de pontuação - Strategy Pattern (Atividade 6)
                'totalScore': stats.get('total_score', 0),
                'avgScore': round(stats.get('avg_score', 0.0), 2),
                'bestStreak': stats.get('best_streak', 0)
            },
            'timestamp': datetime.now().isoformat()
        }


# Instância global (singleton para simplificar)
session_analytics = SessionAnalytics()
