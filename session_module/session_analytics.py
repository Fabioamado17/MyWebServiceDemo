"""
Módulo de Session Analytics - Fábio Amado (2501444)

Integração do padrão Factory Method com tracking de sessões.
Responsável por monitorizar:
- Tempo de jogo por sessão
- Número de sessões
- Interações por desafio
- Dias consecutivos de jogo
- Padrões de uso

Autor: Fábio Amado (2501444@estudante.uab.pt)
"""
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from models.challenge import Challenge


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
            'active': True
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
                'play_dates': []
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
        
        # Atualizar stats do utilizador
        user_id = session['user_id']
        self.user_stats[user_id]['total_challenges'] += 1
        self.user_stats[user_id]['total_interactions'] += 1
    
    def log_challenge_complete(self, session_id: str, challenge_id: str, 
                              is_correct: bool) -> None:
        """
        Regista conclusão de um desafio.
        
        Args:
            session_id: ID da sessão
            challenge_id: ID do desafio
            is_correct: Se a resposta estava correta
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
        
        if start_interaction:
            # Calcular tempo gasto no desafio
            end_time = datetime.now()
            duration = (end_time - start_interaction['start_time']).total_seconds()
            
            session['challenge_times'].append({
                'challenge_id': challenge_id,
                'challenge_type': start_interaction['challenge_type'],
                'duration': duration,
                'is_correct': is_correct
            })
        
        # Registar interação de conclusão
        interaction = {
            'type': 'challenge_complete',
            'challenge_id': challenge_id,
            'is_correct': is_correct,
            'timestamp': datetime.now().isoformat()
        }
        
        session['interactions'].append(interaction)
        self.user_stats[session['user_id']]['total_interactions'] += 1
    
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
        
        # Atualizar stats do utilizador
        user_id = session['user_id']
        self.user_stats[user_id]['total_play_time'] += duration
        
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
            'active': session['active']
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
                )
            },
            'timestamp': datetime.now().isoformat()
        }


# Instância global (singleton para simplificar)
session_analytics = SessionAnalytics()
