"""
Dados de exemplo para os alunos
"""
import random

# Dados pré-definidos para alguns alunos
MOCK_STUDENT_DATA = {
    'student_123': {
        'totalRespostas': 45,
        'respostasCorretas': 37,
        'respostasIncorretas': 8,
        'taxaAcerto': 82,
        'nivelAtual': 3,
        'animaisDescobertos': 12,
        'categoriasCompletadas': 2,
        'totalSessoes': 12,
        'tempoTotalJogo': 180,
        'tempoMedioSessao': 15,
        'interacoesTotais': 156,
        'repeticoesNiveis': 3,
        'diasConsecutivos': 5
    },
    'student_456': {
        'totalRespostas': 30,
        'respostasCorretas': 24,
        'respostasIncorretas': 6,
        'taxaAcerto': 80,
        'nivelAtual': 2,
        'animaisDescobertos': 8,
        'categoriasCompletadas': 1,
        'totalSessoes': 8,
        'tempoTotalJogo': 120,
        'tempoMedioSessao': 15,
        'interacoesTotais': 98,
        'repeticoesNiveis': 2,
        'diasConsecutivos': 4
    }
}


def get_student_data(student_id):
    """
    Retorna dados do aluno. Se não existir, gera dados aleatórios.
    """
    if student_id in MOCK_STUDENT_DATA:
        return MOCK_STUDENT_DATA[student_id]
    
    # Gerar dados aleatórios para aluno não cadastrado
    total_respostas = random.randint(20, 70)
    respostas_corretas = int(total_respostas * random.uniform(0.6, 0.9))
    respostas_incorretas = total_respostas - respostas_corretas
    
    return {
        'totalRespostas': total_respostas,
        'respostasCorretas': respostas_corretas,
        'respostasIncorretas': respostas_incorretas,
        'taxaAcerto': round((respostas_corretas / total_respostas) * 100),
        'nivelAtual': random.randint(1, 5),
        'animaisDescobertos': random.randint(5, 25),
        'categoriasCompletadas': random.randint(1, 5),
        'totalSessoes': random.randint(5, 20),
        'tempoTotalJogo': random.randint(60, 260),
        'tempoMedioSessao': random.randint(10, 30),
        'interacoesTotais': random.randint(50, 250),
        'repeticoesNiveis': random.randint(0, 5),
        'diasConsecutivos': random.randint(1, 8)
    }