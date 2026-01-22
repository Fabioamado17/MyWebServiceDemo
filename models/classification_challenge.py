"""
Desafio de classificação alimentar.

Padrão de Criação: Factory Method (Produto Concreto)
Autor: Fábio Amado (2501444)
"""
from models.challenge import Challenge
from typing import List


class ClassificationChallenge(Challenge):
    """
    Desafio sobre o tipo de alimentação do animal.
    
    O aluno deve classificar o animal como carnívoro, herbívoro ou omnívoro.
    Este é um "Produto Concreto" no padrão Factory Method.
    """
    
    def __init__(self, animal_id: int, difficulty: int = 1):
        """
        Inicializa desafio de classificação.
        
        Args:
            animal_id: ID do animal
            difficulty: Nível de dificuldade
        """
        super().__init__(animal_id, difficulty)
        
        from data.animals_data import get_animal_data
        import random
        
        self.animal_data = get_animal_data(animal_id)
        self.challenge_id = f"class_{animal_id}_{random.randint(1000, 9999)}"
        self.correct_answer = self.animal_data['diet']
    
    def get_question(self) -> str:
        """Retorna a pergunta do desafio"""
        return f"O {self.animal_data['name_pt']} é...?"
    
    def get_options(self) -> List[str]:
        """Retorna as opções de classificação"""
        return ["Carnívoro", "Herbívoro", "Omnívoro"]
    
    def get_challenge_type(self) -> str:
        """Retorna o tipo do desafio"""
        return "classification"
    
    def validate_answer(self, answer: str) -> bool:
        """Valida a resposta do aluno"""
        return answer.strip().lower() == self.correct_answer.lower()
    
    def to_dict(self):
        """Converte para dicionário"""
        data = super().to_dict()
        data['animal_name'] = self.animal_data['name_pt']
        data['animal_image'] = self.animal_data['image_file']
        data['instructions'] = "Classifica o tipo de alimentação deste animal"
        data['hint'] = self._get_hint()
        return data
    
    def _get_hint(self) -> str:
        """Retorna uma dica baseada na classificação"""
        hints = {
            'Carnívoro': 'Este animal alimenta-se principalmente de carne',
            'Herbívoro': 'Este animal alimenta-se principalmente de plantas',
            'Omnívoro': 'Este animal come tanto plantas como carne'
        }
        return hints.get(self.correct_answer, '')
