"""
Classe abstrata base para todos os desafios do jogo.

Padrão de Criação: Factory Method (Produto Abstrato)
Autores: Henrique Crachat (2501450) & Fábio Amado (2501444)
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List


class Challenge(ABC):
    """
    Classe base abstrata para desafios do jogo "Dia & Noite".
    
    Define a interface que todos os desafios concretos devem implementar.
    Esta é a classe "Produto" no padrão Factory Method.
    
    Attributes:
        animal_id (int): ID do animal relacionado ao desafio
        difficulty (int): Nível de dificuldade (1-5)
        challenge_id (str): Identificador único do desafio
        correct_answer (str): Resposta correta do desafio
    """
    
    def __init__(self, animal_id: int, difficulty: int = 1):
        """
        Inicializa um desafio.
        
        Args:
            animal_id: ID do animal para este desafio
            difficulty: Nível de dificuldade (padrão: 1)
        """
        self.animal_id = animal_id
        self.difficulty = difficulty
        self.challenge_id = None
        self.correct_answer = None
    
    @abstractmethod
    def get_question(self) -> str:
        """
        Retorna a pergunta do desafio.
        
        Returns:
            String com a pergunta a apresentar ao aluno
        """
        pass
    
    @abstractmethod
    def get_options(self) -> List[str]:
        """
        Retorna as opções de resposta.
        
        Returns:
            Lista com as opções de resposta (incluindo a correta)
        """
        pass
    
    @abstractmethod
    def get_challenge_type(self) -> str:
        """
        Retorna o tipo do desafio.
        
        Returns:
            String identificando o tipo ('audio', 'visual', etc.)
        """
        pass
    
    @abstractmethod
    def validate_answer(self, answer: str) -> bool:
        """
        Valida se a resposta do aluno está correta.
        
        Args:
            answer: Resposta fornecida pelo aluno
            
        Returns:
            True se a resposta está correta, False caso contrário
        """
        pass
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Converte o desafio para formato dicionário (JSON).
        
        Returns:
            Dicionário com todos os dados do desafio
        """
        return {
            'challenge_id': self.challenge_id,
            'animal_id': self.animal_id,
            'type': self.get_challenge_type(),
            'difficulty': self.difficulty,
            'question': self.get_question(),
            'options': self.get_options()
        }
    
    def __repr__(self) -> str:
        """Representação em string do desafio"""
        return f"{self.__class__.__name__}(animal_id={self.animal_id}, difficulty={self.difficulty})"
