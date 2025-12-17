"""
Decorator para adicionar limite de tempo aos desafios.

Padrão Estrutural: Decorator (Concrete Decorator)
Adiciona funcionalidade de cronometragem e tempo limite aos desafios.

Autores: Henrique Crachat (2501450) & Fábio Amado (2501444)
UC: Arquitetura e Padrões de Software
Universidade Aberta
"""
from decorators.challenge_decorator import ChallengeDecorator
from models.challenge import Challenge
from typing import Dict, Any
import time


class TimedDecorator(ChallengeDecorator):
    """
    Decorator que adiciona limite de tempo aos desafios.

    PADRÃO ESTRUTURAL: Decorator (Concrete Decorator)

    Funcionalidades Adicionadas:
    ---------------------------
    1. **Limite de Tempo**: Define tempo máximo para completar o desafio
    2. **Cronometragem**: Rastreia quando o desafio começou
    3. **Tempo Restante**: Calcula quanto tempo resta
    4. **Expiração**: Verifica se o tempo acabou
    5. **Bónus de Velocidade**: Calcula pontos extra por rapidez
    6. **Penalização por Timeout**: Detecta respostas fora do tempo

    Propósito Educativo:
    ------------------
    - Aumenta dificuldade progressivamente
    - Mede fluência do conhecimento (resposta rápida = domínio)
    - Gamificação: pontos bónus por velocidade
    - Analytics: identifica conceitos que demoram mais

    Example:
    -------
    >>> from factories.challenge_factory import ChallengeFactory
    >>> from decorators.timed_decorator import TimedDecorator
    >>>
    >>> # Criar desafio básico
    >>> base = ChallengeFactory.create_challenge('audio', animal_id=1)
    >>>
    >>> # Decorar com limite de tempo
    >>> timed = TimedDecorator(base, time_limit=30)
    >>>
    >>> # Iniciar cronometragem
    >>> timed.start_timer()
    >>>
    >>> # Verificar tempo restante
    >>> if not timed.is_expired():
    ...     time_left = timed.get_time_remaining()
    ...     print(f"Tens {time_left:.1f} segundos!")
    >>>
    >>> # Calcular bónus por velocidade
    >>> bonus = timed.calculate_time_bonus(time_taken=15.5)
    """

    def __init__(self, challenge: Challenge, time_limit: float = 30.0):
        """
        Inicializa o decorator de tempo.

        Args:
            challenge: Desafio a decorar
            time_limit: Tempo limite em segundos (padrão: 30s)

        Raises:
            ValueError: Se time_limit for negativo ou zero
        """
        super().__init__(challenge)

        if time_limit <= 0:
            raise ValueError("time_limit deve ser positivo")

        self.time_limit = time_limit
        self._start_time = None
        self._end_time = None

    def start_timer(self) -> None:
        """
        Inicia o cronómetro do desafio.

        Este método deve ser chamado quando o desafio é apresentado ao aluno.

        Example:
            >>> timed_challenge.start_timer()
            >>> # Aluno responde ao desafio...
            >>> time_taken = timed_challenge.get_elapsed_time()
        """
        self._start_time = time.time()
        self._end_time = None

    def stop_timer(self) -> float:
        """
        Para o cronómetro e retorna o tempo decorrido.

        Returns:
            Tempo decorrido em segundos

        Raises:
            RuntimeError: Se o cronómetro não foi iniciado
        """
        if self._start_time is None:
            raise RuntimeError("Cronómetro não foi iniciado. Chama start_timer() primeiro.")

        self._end_time = time.time()
        return self.get_elapsed_time()

    def get_elapsed_time(self) -> float:
        """
        Retorna o tempo decorrido desde o início.

        Returns:
            Tempo em segundos desde start_timer()

        Raises:
            RuntimeError: Se o cronómetro não foi iniciado
        """
        if self._start_time is None:
            raise RuntimeError("Cronómetro não foi iniciado. Chama start_timer() primeiro.")

        if self._end_time is not None:
            # Cronómetro já foi parado
            return self._end_time - self._start_time
        else:
            # Cronómetro ainda a correr
            return time.time() - self._start_time

    def get_time_remaining(self) -> float:
        """
        Retorna o tempo restante para completar o desafio.

        Returns:
            Tempo restante em segundos (0 se expirado)

        Raises:
            RuntimeError: Se o cronómetro não foi iniciado

        Example:
            >>> remaining = timed_challenge.get_time_remaining()
            >>> if remaining > 0:
            ...     print(f"Despacha-te! {remaining:.1f}s restantes!")
        """
        elapsed = self.get_elapsed_time()
        remaining = self.time_limit - elapsed
        return max(0, remaining)  # Nunca retorna negativo

    def is_expired(self) -> bool:
        """
        Verifica se o tempo limite foi excedido.

        Returns:
            True se o tempo acabou, False caso contrário

        Raises:
            RuntimeError: Se o cronómetro não foi iniciado

        Example:
            >>> if timed_challenge.is_expired():
            ...     print("Tempo esgotado! Resposta não conta.")
        """
        if self._start_time is None:
            raise RuntimeError("Cronómetro não foi iniciado. Chama start_timer() primeiro.")

        return self.get_elapsed_time() >= self.time_limit

    def is_timer_running(self) -> bool:
        """
        Verifica se o cronómetro está a correr.

        Returns:
            True se o cronómetro foi iniciado e não foi parado
        """
        return self._start_time is not None and self._end_time is None

    def calculate_time_bonus(self, time_taken: float = None) -> int:
        """
        Calcula pontos bónus baseado na velocidade de resposta.

        Fórmula:
        -------
        - 100 pontos se completar em 25% do tempo
        - 50 pontos se completar em 50% do tempo
        - 25 pontos se completar em 75% do tempo
        - 0 pontos se completar em >75% do tempo ou timeout

        Args:
            time_taken: Tempo gasto (usa elapsed_time se None)

        Returns:
            Pontos bónus (0-100)

        Example:
            >>> # Completou em 10s de um limite de 30s
            >>> bonus = timed_challenge.calculate_time_bonus(10)
            >>> print(bonus)  # 100 pontos (33% do tempo)
        """
        if time_taken is None:
            time_taken = self.get_elapsed_time()

        # Se excedeu o limite, sem bónus
        if time_taken >= self.time_limit:
            return 0

        # Calcular percentagem do tempo usado
        time_percentage = time_taken / self.time_limit

        if time_percentage <= 0.25:
            return 100  # Muito rápido!
        elif time_percentage <= 0.50:
            return 50   # Rápido
        elif time_percentage <= 0.75:
            return 25   # Moderado
        else:
            return 0    # Lento

    def get_time_performance_level(self) -> str:
        """
        Retorna nível de desempenho baseado no tempo.

        Returns:
            String: 'excellent', 'good', 'fair', 'timeout'

        Example:
            >>> performance = timed_challenge.get_time_performance_level()
            >>> if performance == 'excellent':
            ...     print("Incrível! Super rápido!")
        """
        if self._start_time is None:
            return 'not_started'

        elapsed = self.get_elapsed_time()
        time_percentage = elapsed / self.time_limit

        if time_percentage > 1.0:
            return 'timeout'
        elif time_percentage <= 0.25:
            return 'excellent'
        elif time_percentage <= 0.50:
            return 'good'
        elif time_percentage <= 0.75:
            return 'fair'
        else:
            return 'slow'

    def validate_answer(self, answer: str) -> bool:
        """
        Valida resposta e automaticamente para o cronómetro.

        Args:
            answer: Resposta do aluno

        Returns:
            True se correto, False se incorreto ou timeout

        Note:
            Para o cronómetro automaticamente quando chamado.
            Se o tempo expirou, retorna False independentemente da resposta.
        """
        # Para o cronómetro se ainda estiver a correr
        if self.is_timer_running():
            self.stop_timer()

        # Se expirou, resposta não conta
        if self.is_expired():
            return False

        # Delegar validação ao desafio decorado
        return self._challenge.validate_answer(answer)

    def to_dict(self) -> Dict[str, Any]:
        """
        Converte para dicionário incluindo informações de tempo.

        Returns:
            Dicionário com dados do desafio + informações de tempo
        """
        # Obter dados base do desafio decorado
        data = super().to_dict()

        # Adicionar informações de tempo
        data['timed'] = True
        data['time_limit'] = self.time_limit

        # Se cronómetro iniciado, adicionar informações de tempo
        if self._start_time is not None:
            data['elapsed_time'] = round(self.get_elapsed_time(), 2)
            data['time_remaining'] = round(self.get_time_remaining(), 2)
            data['is_expired'] = self.is_expired()
            data['time_performance'] = self.get_time_performance_level()

            # Se completado, adicionar bónus
            if self._end_time is not None:
                data['time_bonus'] = self.calculate_time_bonus()

        return data

    def reset_timer(self) -> None:
        """
        Reinicia o cronómetro (útil para retry).

        Example:
            >>> timed_challenge.reset_timer()
            >>> timed_challenge.start_timer()  # Novo attempt
        """
        self._start_time = None
        self._end_time = None

    def __repr__(self) -> str:
        """Representação em string"""
        status = "running" if self.is_timer_running() else "stopped"
        return f"TimedDecorator({self._challenge}, limit={self.time_limit}s, status={status})"
