"""
Gestor de Sessões - Componente SRP.

Responsabilidade Única: Criar e terminar sessões.

Autor: Fábio Amado (2501444)
"""
from typing import Dict, List, Optional
from datetime import datetime


class SessionManager:
    """
    Gere o ciclo de vida das sessões.

    Responsabilidades:
    - Criar novas sessões
    - Terminar sessões existentes
    - Verificar estado das sessões
    - Manter referências user_id -> session_ids
    """

    def __init__(self):
        """Inicializa o gestor de sessões."""
        # {session_id: {dados da sessão}}
        self.sessions: Dict[str, Dict] = {}
        # {user_id: [session_ids]}
        self.user_sessions: Dict[str, List[str]] = {}

    def create_session(self, user_id: str,
                      session_id: Optional[str] = None) -> str:
        """
        Cria uma nova sessão.

        Args:
            user_id: Identificador do utilizador
            session_id: ID personalizado (opcional)

        Returns:
            ID da sessão criada
        """
        if session_id is None:
            session_id = f"{user_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"

        self.sessions[session_id] = {
            'session_id': session_id,
            'user_id': user_id,
            'start_time': datetime.now().isoformat(),
            'end_time': None,
            'duration': 0,
            'challenges_attempted': 0,
            'interactions': [],
            'challenge_times': [],
            'active': True,
            # Campos para scoring (Strategy Pattern)
            'current_streak': 0,
            'current_challenge_attempts': {},
            'scores': [],
            'total_score': 0
        }

        # Registar sessão do utilizador
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = []
        self.user_sessions[user_id].append(session_id)

        return session_id

    def end_session(self, session_id: str) -> Dict:
        """
        Termina uma sessão.

        Args:
            session_id: ID da sessão

        Returns:
            Dados atualizados da sessão

        Raises:
            ValueError: Se sessão não existe
        """
        if session_id not in self.sessions:
            raise ValueError(f"Sessão {session_id} não encontrada")

        session = self.sessions[session_id]

        if not session['active']:
            return session

        # Calcular duração
        start = datetime.fromisoformat(session['start_time'])
        end = datetime.now()
        duration = (end - start).total_seconds()

        session['end_time'] = end.isoformat()
        session['duration'] = duration
        session['active'] = False

        return session

    def get_session(self, session_id: str) -> Dict:
        """
        Obtém dados de uma sessão.

        Args:
            session_id: ID da sessão

        Returns:
            Dados da sessão

        Raises:
            ValueError: Se sessão não existe
        """
        if session_id not in self.sessions:
            raise ValueError(f"Sessão {session_id} não encontrada")
        return self.sessions[session_id]

    def is_session_active(self, session_id: str) -> bool:
        """Verifica se sessão está ativa."""
        if session_id not in self.sessions:
            return False
        return self.sessions[session_id]['active']

    def get_user_sessions(self, user_id: str) -> List[str]:
        """Retorna lista de sessões de um utilizador."""
        return self.user_sessions.get(user_id, [])
