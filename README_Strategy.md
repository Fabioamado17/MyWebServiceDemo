# Strategy Pattern - Sistema de Pontuação

**Padrão de Comportamento implementado na Atividade 6**

**Autor:** Fábio Amado (2501444)

---

## O que é o Strategy Pattern?

O **Strategy Pattern** é um padrão de design comportamental que permite definir uma família de algoritmos, encapsular cada um deles e torná-los intercambiáveis. O Strategy permite que o algoritmo varie independentemente dos clientes que o utilizam.

### Analogia Simples

Imagina que és um professor e tens diferentes formas de avaliar os alunos:
- Num teste rápido, avalias pela **velocidade**
- Num trabalho de casa, avalias pela **precisão** (acertar à primeira)
- Numa maratona de exercícios, avalias pela **consistência** (manter streak)
- Num exame final, avalias pela **dificuldade** das questões

Em vez de ter um método gigante cheio de `if/else` para decidir como pontuar, o Strategy Pattern permite trocar o "algoritmo de avaliação" como se estivesses a trocar de régua.

---

## Problema Resolvido

### Antes (Sem Strategy)

```python
def calculate_score(context):
    if scoring_type == 'time':
        if time_percentage <= 25:
            return 100
        elif time_percentage <= 50:
            return 75
        # ... mais ifs
    elif scoring_type == 'accuracy':
        if attempts == 1:
            return 100
        elif attempts == 2:
            return 60
        # ... mais ifs
    elif scoring_type == 'streak':
        # ... mais ifs
    # Código difícil de manter e estender!
```

### Depois (Com Strategy)

```python
calculator.set_strategy(TimeBasedScoringStrategy())
score = calculator.calculate(context)  # Limpo e flexível!

# Trocar estratégia é trivial
calculator.set_strategy(AccuracyScoringStrategy())
score = calculator.calculate(context)  # Mesmo contexto, novo algoritmo!
```

---

## Estrutura do Padrão

### Componentes

1. **Strategy (Interface)** - `ScoringStrategy`
   - Define o contrato: `calculate_score(context) -> int`
   - Todas as estratégias implementam esta interface

2. **Concrete Strategies** - Implementações específicas
   - `TimeBasedScoringStrategy` - Pontos baseados em velocidade
   - `AccuracyScoringStrategy` - Pontos baseados em tentativas
   - `StreakScoringStrategy` - Pontos baseados em sequência de acertos
   - `DifficultyBasedScoringStrategy` - Pontos ajustados por dificuldade
   - `CompositeScoringStrategy` - Combina múltiplas estratégias

3. **Context** - `ScoreCalculator`
   - Mantém referência para a estratégia atual
   - Delega o cálculo para a estratégia
   - Permite trocar estratégia em runtime

4. **Client** - `SessionAnalytics`
   - Usa o Context sem conhecer a estratégia concreta
   - Prepara o contexto com os dados necessários

### Diagrama Simplificado

```
┌─────────────────────────┐
│   ScoringStrategy       │
│   (Interface)           │
│  + calculate_score()    │
└───────────┬─────────────┘
            │ implements
    ┌───────┴────────┬──────────────┬──────────────┐
    │                │              │              │
┌───▼────┐  ┌────────▼───┐  ┌──────▼─────┐  ┌────▼─────┐
│ Time   │  │ Accuracy   │  │  Streak    │  │Composite │
│ Based  │  │  Based     │  │   Based    │  │          │
└────────┘  └────────────┘  └────────────┘  └──────────┘

┌─────────────────────────────────────┐
│      ScoreCalculator                │
│      (Context)                      │
│  - strategy: ScoringStrategy        │
│  + set_strategy(strategy)           │
│  + calculate(context) -> int        │
└─────────────────────────────────────┘
```

---

## Estratégias Implementadas

### 1. TimeBasedScoringStrategy

Recompensa respostas rápidas.

**Fórmula:**
- ≤ 25% do tempo → 100 pontos
- ≤ 50% do tempo → 75 pontos
- ≤ 75% do tempo → 50 pontos
- > 75% do tempo → 25 pontos
- Timeout → 0 pontos

**Exemplo:**
```python
context = {'time_taken': 10, 'time_limit': 30, 'is_correct': True}
# 10/30 = 33% → 75 pontos
```

### 2. AccuracyScoringStrategy

Recompensa acertar à primeira tentativa.

**Fórmula:**
- 1ª tentativa → 100 pontos
- 2ª tentativa → 60 pontos
- 3ª tentativa → 30 pontos
- 4+ tentativas → 0 pontos

**Exemplo:**
```python
context = {'attempts': 1, 'is_correct': True}
# Primeira tentativa → 100 pontos
```

### 3. StreakScoringStrategy

Recompensa sequências de acertos consecutivos.

**Fórmula:**
- Base: 50 pontos (se correto)
- Streak 2-3 → +10 pontos
- Streak 4-5 → +20 pontos
- Streak 6-9 → +30 pontos
- Streak 10+ → +50 pontos

**Exemplo:**
```python
context = {'streak': 5, 'is_correct': True}
# 50 (base) + 20 (streak 4-5) = 70 pontos
```

### 4. DifficultyBasedScoringStrategy

Ajusta pontos pela dificuldade do desafio.

**Fórmula:**
- Dificuldade 1 (fácil) → 40 pontos
- Dificuldade 2 → 60 pontos
- Dificuldade 3 (médio) → 80 pontos
- Dificuldade 4 → 90 pontos
- Dificuldade 5 (difícil) → 100 pontos

**Exemplo:**
```python
context = {'difficulty': 5, 'is_correct': True}
# Dificuldade 5 → 100 pontos
```

### 5. CompositeScoringStrategy

Combina múltiplas estratégias com pesos configuráveis.

**Fórmula:**
```
score_final = (strategy1_score × weight1) + (strategy2_score × weight2) + ...
```

**Configuração Padrão:**
```python
CompositeScoringStrategy([
    (TimeBasedScoringStrategy(), 0.4),    # 40% peso
    (AccuracyScoringStrategy(), 0.4),     # 40% peso
    (StreakScoringStrategy(), 0.2)        # 20% peso
])
```

**Exemplo:**
```python
# Time: 75 pts, Accuracy: 100 pts, Streak: 60 pts
# Final = (75 × 0.4) + (100 × 0.4) + (60 × 0.2)
#       = 30 + 40 + 12 = 82 pontos
```

---

## Como Usar

### Uso Básico

```python
from strategies.score_calculator import ScoreCalculator
from strategies.time_based_scoring import TimeBasedScoringStrategy

# Criar calculador com estratégia
calculator = ScoreCalculator(TimeBasedScoringStrategy())

# Preparar contexto
context = {
    'time_taken': 10,
    'time_limit': 30,
    'is_correct': True,
    'attempts': 1,
    'difficulty': 3,
    'streak': 5
}

# Calcular pontuação
score = calculator.calculate(context)
print(f"Pontuação: {score}")  # 75
```

### Trocar Estratégia em Runtime

```python
# Começar com uma estratégia
calculator.set_strategy(TimeBasedScoringStrategy())
score1 = calculator.calculate(context)  # 75

# Trocar para outra estratégia
calculator.set_strategy(AccuracyScoringStrategy())
score2 = calculator.calculate(context)  # 100

# Mesmo contexto, scores diferentes!
```

### Obter Resultado Detalhado

```python
result = calculator.get_detailed_result(context)
print(result)
# {
#   'score': 82,
#   'performance': 'good',
#   'strategy': 'composite(...)',
#   'context': {...}
# }
```

### Integração com SessionAnalytics

```python
from session_module.session_analytics import session_analytics
from factories.challenge_factory import ChallengeFactory

# Iniciar sessão
session_id = session_analytics.start_session('student123')

# Criar desafio
challenge = ChallengeFactory.create_challenge('audio', animal_id=1)
session_analytics.log_challenge_start(session_id, challenge)

# Completar desafio (pontuação calculada automaticamente)
score_result = session_analytics.log_challenge_complete(
    session_id,
    challenge.challenge_id,
    is_correct=True,
    difficulty=3,
    time_limit=30
)

print(f"Score: {score_result['score']}")
print(f"Performance: {score_result['performance']}")
```

---

## Testar o Padrão

### Executar Todos os Testes

```bash
python test_strategy_pattern.py
```

### Testes Incluídos

1. **Teste 1:** TimeBasedScoringStrategy
2. **Teste 2:** AccuracyScoringStrategy
3. **Teste 3:** StreakScoringStrategy
4. **Teste 4:** DifficultyBasedScoringStrategy
5. **Teste 5:** CompositeScoringStrategy (com breakdown)
6. **Teste 6:** Strategy Switching (trocar em runtime)
7. **Teste 7:** Integração com SessionAnalytics

### Testar Interativamente

```python
python

>>> from strategies.score_calculator import ScoreCalculator
>>> from strategies.time_based_scoring import TimeBasedScoringStrategy
>>>
>>> calc = ScoreCalculator(TimeBasedScoringStrategy())
>>> context = {'time_taken': 5, 'time_limit': 30, 'is_correct': True}
>>> calc.calculate(context)
100
```

---

## Criar Nova Estratégia

É muito fácil adicionar novas estratégias sem modificar código existente:

```python
from strategies.scoring_strategy import ScoringStrategy
from typing import Dict, Any

class HintPenaltyScoringStrategy(ScoringStrategy):
    """Penaliza uso de dicas"""

    def calculate_score(self, context: Dict[str, Any]) -> int:
        base_score = 100 if context.get('is_correct') else 0
        hints_used = context.get('hints_used', 0)
        penalty = hints_used * 15  # -15 pontos por dica
        return max(base_score - penalty, 0)

    def get_strategy_name(self) -> str:
        return "hint_penalty"

# Usar imediatamente!
calculator.set_strategy(HintPenaltyScoringStrategy())
```

**Nenhuma modificação** necessária em:
- ScoreCalculator
- SessionAnalytics
- Outras estratégias
- Código cliente

Isto demonstra o **Open/Closed Principle**: aberto para extensão, fechado para modificação.

---

## Vantagens do Padrão

### Princípios SOLID

- **Single Responsibility:** Cada estratégia tem uma responsabilidade
- **Open/Closed:** Adicionar estratégias sem modificar código existente
- **Dependency Inversion:** Código depende de abstrações (ScoringStrategy)

### Benefícios Práticos

- Elimina blocos `if/else` complexos
- Permite trocar algoritmo em runtime
- Fácil de testar (cada estratégia independente)
- Código reutilizável
- Fácil de estender

### Comparação: Sem vs Com Strategy

| Aspeto | Sem Strategy | Com Strategy |
|--------|--------------|--------------|
| Adicionar novo algoritmo | Modificar código existente | Criar nova classe |
| Trocar algoritmo | Alterar variável + rebuild | `set_strategy()` |
| Testar | Testar método gigante | Testar cada estratégia |
| Manutenção | Código acoplado | Código desacoplado |

---

## Integração com Outros Padrões

O Strategy trabalha em harmonia com os outros padrões implementados:

```python
# 1. Factory cria o desafio
challenge = ChallengeFactory.create_challenge('visual', animal_id=2)

# 2. Decorator adiciona funcionalidades
timed = TimedDecorator(challenge, time_limit=30)

# 3. Strategy calcula pontuação
score_result = session_analytics.log_challenge_complete(
    session_id,
    timed.challenge_id,
    is_correct=True
)
```

**Separação de Responsabilidades:**
- **Factory Method:** Cria desafios
- **Decorator:** Adiciona funcionalidades
- **Strategy:** Define comportamento de pontuação

Todos mantêm a mesma interface base, permitindo composição flexível.

---

## Ficheiros do Padrão

```
strategies/
├── __init__.py                    # Exports do módulo
├── scoring_strategy.py            # Interface Strategy
├── time_based_scoring.py          # Estratégia: Tempo
├── accuracy_scoring.py            # Estratégia: Precisão
├── streak_scoring.py              # Estratégia: Streak
├── difficulty_scoring.py          # Estratégia: Dificuldade
├── composite_scoring.py           # Estratégia: Composta
└── score_calculator.py            # Context

session_module/
└── session_analytics.py           # Cliente (integrado)

test_strategy_pattern.py           # Testes completos

Diagramas/Diagramas_Atividade6/
├── DiagramaComponentes_AtividadeCompleta.md
├── DiagramaSequencia_StrategyPattern.md
└── DiagramaEstrutura_StrategyPattern.md
```

---

## Configuração Atual

O sistema usa por padrão uma estratégia composta que equilibra:
- **40% Tempo:** Recompensa rapidez
- **40% Precisão:** Recompensa acertar à primeira
- **20% Streak:** Recompensa consistência

Esta configuração pode ser alterada facilmente:

```python
from session_module.session_analytics import session_analytics
from strategies.difficulty_scoring import DifficultyBasedScoringStrategy

# Mudar para pontuação baseada apenas em dificuldade
session_analytics.score_calculator.set_strategy(
    DifficultyBasedScoringStrategy()
)
```

---

## Métricas Exportadas

O sistema agora exporta métricas de pontuação para a plataforma Inven!RA:

```json
{
  "studentId": "student123",
  "activityId": "dia-noite-animals",
  "sessionMetrics": {
    "totalSessions": 12,
    "totalScore": 4250,
    "avgScore": 73.28,
    "bestStreak": 12,
    ...
  }
}
```

---

## Recursos Adicionais

- **Documentação da Atividade 6:** `Diagramas/Diagramas_Atividade6/README.md`
- **Comparação com Observer:** `Comparacao_Observer_vs_Strategy.txt`
- **Diagramas Mermaid:** `Diagramas/Diagramas_Atividade6/`

---

## Conclusão

O **Strategy Pattern** torna o sistema de pontuação:
- **Flexível:** Trocar algoritmos facilmente
- **Extensível:** Adicionar novas estratégias sem modificar código
- **Testável:** Cada estratégia testada independentemente
- **Manutenível:** Código organizado e desacoplado

Este padrão complementa perfeitamente o Factory Method (criação) e o Decorator (estrutura), completando uma arquitetura robusta baseada em padrões de design.
