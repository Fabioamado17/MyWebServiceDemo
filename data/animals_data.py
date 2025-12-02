"""
Base de dados mockup com informações dos animais.

Contém dados de animais para os desafios do jogo "Dia & Noite".

Autores: Henrique Crachat (2501450) & Fábio Amado (2501444)
"""
import random
from typing import List, Dict, Optional


# Habitats disponíveis no jogo
HABITATS = {
    'floresta': 'Floresta Tropical',
    'savana': 'Savana Africana',
    'oceano': 'Oceano',
    'deserto': 'Deserto',
    'montanha': 'Montanhas',
    'polo': 'Regiões Polares'
}

# Base de dados de animais
ANIMALS_DB = [
    {
        'id': 1,
        'name_pt': 'Leão',
        'name_en': 'Lion',
        'habitat': 'savana',
        'period': 'diurno',
        'diet': 'Carnívoro',
        'sound_file': 'sounds/leao.mp3',
        'image_file': 'images/leao.jpg',
        'fun_fact': 'O rugido do leão pode ser ouvido a até 8 km de distância!'
    },
    {
        'id': 2,
        'name_pt': 'Elefante',
        'name_en': 'Elephant',
        'habitat': 'savana',
        'period': 'diurno',
        'diet': 'Herbívoro',
        'sound_file': 'sounds/elefante.mp3',
        'image_file': 'images/elefante.jpg',
        'fun_fact': 'Os elefantes podem comunicar através de infrasom que humanos não ouvem.'
    },
    {
        'id': 3,
        'name_pt': 'Coruja',
        'name_en': 'Owl',
        'habitat': 'floresta',
        'period': 'noturno',
        'diet': 'Carnívoro',
        'sound_file': 'sounds/coruja.mp3',
        'image_file': 'images/coruja.jpg',
        'fun_fact': 'As corujas podem girar a cabeça até 270 graus!'
    },
    {
        'id': 4,
        'name_pt': 'Macaco',
        'name_en': 'Monkey',
        'habitat': 'floresta',
        'period': 'diurno',
        'diet': 'Omnívoro',
        'sound_file': 'sounds/macaco.mp3',
        'image_file': 'images/macaco.jpg',
        'fun_fact': 'Macacos podem usar ferramentas para obter comida.'
    },
    {
        'id': 5,
        'name_pt': 'Golfinho',
        'name_en': 'Dolphin',
        'habitat': 'oceano',
        'period': 'diurno',
        'diet': 'Carnívoro',
        'sound_file': 'sounds/golfinho.mp3',
        'image_file': 'images/golfinho.jpg',
        'fun_fact': 'Golfinhos dormem com metade do cérebro de cada vez.'
    }
]


def get_animal_data(animal_id: int) -> Dict:
    """Buscar dados de um animal pelo ID"""
    for animal in ANIMALS_DB:
        if animal['id'] == animal_id:
            return animal.copy()
    raise ValueError(f"Animal com ID {animal_id} não encontrado")


def get_random_animals(habitat: Optional[str] = None, 
                       exclude_id: Optional[int] = None, 
                       count: int = 3) -> List[Dict]:
    """Buscar animais aleatórios, opcionalmente filtrados por habitat"""
    animals = ANIMALS_DB.copy()
    
    if habitat:
        animals = [a for a in animals if a['habitat'] == habitat]
    
    if exclude_id is not None:
        animals = [a for a in animals if a['id'] != exclude_id]
    
    sample_size = min(count, len(animals))
    
    if sample_size == 0:
        return []
    
    return [animal.copy() for animal in random.sample(animals, sample_size)]
