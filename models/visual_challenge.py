"""
Desafio de identificação visual.

Padrão de Criação: Factory Method (Produto Concreto)
Autor: Fábio Amado (2501444)
"""
from models.challenge import Challenge
from typing import List
import random


class VisualChallenge(Challenge):
    """
    Desafio baseado na imagem do animal.
    
    O aluno vê uma imagem e deve identificar o animal.
    Este é um "Produto Concreto" no padrão Factory Method.
    """
    
    def __init__(self, animal_id: int, difficulty: int = 1):
        """
        Inicializa desafio visual.
        
        Args:
            animal_id: ID do animal
            difficulty: Nível de dificuldade
        """
        super().__init__(animal_id, difficulty)
        
        from data.animals_data import get_animal_data, get_random_animals
        
        self.animal_data = get_animal_data(animal_id)
        self.challenge_id = f"visual_{animal_id}_{random.randint(1000, 9999)}"
        self.correct_answer = self.animal_data['name_pt']
        self.image_file = self.animal_data['image_file']
        
        self._generate_options = lambda: self._create_options(get_random_animals)
    
    def _create_options(self, get_random_animals_func) -> List[str]:
        """Gera opções de resposta com animais similares"""
        similar_animals = get_random_animals_func(
            habitat=self.animal_data['habitat'],
            exclude_id=self.animal_id,
            count=3
        )
        
        options = [self.correct_answer] + [a['name_pt'] for a in similar_animals]
        random.shuffle(options)
        return options
    
    def get_question(self) -> str:
        """Retorna a pergunta do desafio"""
        return "Como se chama este animal?"
    
    def get_options(self) -> List[str]:
        """Retorna as opções de resposta"""
        return self._generate_options()
    
    def get_challenge_type(self) -> str:
        """Retorna o tipo do desafio"""
        return "visual"
    
    def validate_answer(self, answer: str) -> bool:
        """Valida a resposta do aluno"""
        return answer.strip().lower() == self.correct_answer.lower()
    
    def to_dict(self):
        """Converte para dicionário incluindo ficheiro de imagem"""
        data = super().to_dict()
        data['image_file'] = self.image_file
        data['instructions'] = "Observa a imagem e identifica o animal"
        return data
