"""
Desafio de identificação de habitat.

Padrão de Criação: Factory Method (Produto Concreto)
Autores: Henrique Crachat (2501450) & Fábio Amado (2501444)
"""
from models.challenge import Challenge
from typing import List
import random


class HabitatChallenge(Challenge):
    """
    Desafio sobre o habitat do animal.
    
    O aluno deve identificar onde o animal vive.
    Este é um "Produto Concreto" no padrão Factory Method.
    """
    
    def __init__(self, animal_id: int, difficulty: int = 1):
        """
        Inicializa desafio de habitat.
        
        Args:
            animal_id: ID do animal
            difficulty: Nível de dificuldade
        """
        super().__init__(animal_id, difficulty)
        
        from data.animals_data import get_animal_data, HABITATS
        
        self.animal_data = get_animal_data(animal_id)
        self.challenge_id = f"habitat_{animal_id}_{random.randint(1000, 9999)}"
        self.correct_answer = HABITATS[self.animal_data['habitat']]
        self.habitat_options = HABITATS
    
    def get_question(self) -> str:
        """Retorna a pergunta do desafio"""
        return f"Onde vive o {self.animal_data['name_pt']}?"
    
    def get_options(self) -> List[str]:
        """Retorna as opções de habitat"""
        options = list(self.habitat_options.values())
        random.shuffle(options)
        return options[:4]  # Retornar apenas 4 opções
    
    def get_challenge_type(self) -> str:
        """Retorna o tipo do desafio"""
        return "habitat"
    
    def validate_answer(self, answer: str) -> bool:
        """Valida a resposta do aluno"""
        return answer.strip().lower() == self.correct_answer.lower()
    
    def to_dict(self):
        """Converte para dicionário"""
        data = super().to_dict()
        data['animal_name'] = self.animal_data['name_pt']
        data['animal_image'] = self.animal_data['image_file']
        data['instructions'] = "Seleciona o habitat onde este animal vive"
        return data
