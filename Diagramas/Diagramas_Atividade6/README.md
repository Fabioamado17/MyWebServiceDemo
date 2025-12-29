# Atividade 6 - Padrões de Comportamento
## Strategy Pattern - Sistema de Pontuação

**Autores:** Henrique Crachat (2501450) & Fábio Amado (2501444)
**UC:** Arquitetura e Padrões de Software - Universidade Aberta
**Data:** Dezembro 2024

---

## Índice
1. [Oportunidade Identificada](#oportunidade-identificada)
2. [Padrão Implementado](#padrão-implementado)
3. [Estrutura do Código](#estrutura-do-código)
4. [Diagramas](#diagramas)
5. [Como Testar](#como-testar)
6. [Integração com Padrões Anteriores](#integração-com-padrões-anteriores)

---

## Oportunidade Identificada

### Problema
O Activity Provider "Dia & Noite: O Mundo dos Animais" precisava de um **sistema de pontuação flexível** que pudesse:
- Avaliar desempenho dos alunos de diferentes formas (tempo, precisão, consistência)
- Ser configurável pela plataforma Inven!RA
- Permitir fácil adição de novos critérios de pontuação
- Combinar múltiplos fatores de forma ponderada

### Contexto Educacional
Diferentes contextos educacionais valorizam diferentes aspetos:
- **Jogos de velocidade**: Pontuação baseada em tempo
- **Exercícios de precisão**: Pontuação baseada em tentativas
- **Desafios progressivos**: Pontuação ajustada por dificuldade
- **Sistemas gamificados**: Bónus por streaks de acertos

### Solução: Strategy Pattern
O **Strategy Pattern** permite definir uma família de algoritmos de pontuação intercambiáveis, encapsulando cada um de forma independente e tornando-os substituíveis sem modificar o código cliente.

---

## Padrão Implementado

### Estrutura do Strategy Pattern

```
┌─────────────────────────────────────────────────┐
│         ScoringStrategy (Interface)             │
│  + calculate_score(context) -> int             │
│  + get_strategy_name() -> str                  │
│  + get_performance_level(score) -> str         │
└──────────────────┬──────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
┌───────▼─────────┐  ┌────────▼────────┐
│ TimeBasedScoring│  │ AccuracyScoring │ ...
│    Strategy     │  │    Strategy     │
└─────────────────┘  └─────────────────┘

┌─────────────────────────────────────────────────┐
│      ScoreCalculator (Context)                  │
│  - strategy: ScoringStrategy                    │
│  + set_strategy(strategy)                       │
│  + calculate(context) -> int                    │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│      SessionAnalytics (Client)                  │
│  - score_calculator: ScoreCalculator            │
│  + log_challenge_complete(...) -> Dict          │
└─────────────────────────────────────────────────┘
```

### Participantes

1. **Strategy (Interface)**: `ScoringStrategy`
   - Define contrato para todas as estratégias
   - Método abstrato: `calculate_score(context)`

2. **Concrete Strategies**: 5 implementações
   - `TimeBasedScoringStrategy` - Velocidade
   - `AccuracyScoringStrategy` - Precisão
   - `StreakScoringStrategy` - Consistência
   - `DifficultyBasedScoringStrategy` - Dificuldade
   - `CompositeScoringStrategy` - Combinação ponderada

3. **Context**: `ScoreCalculator`
   - Mantém referência para estratégia atual
   - Permite trocar estratégia em runtime
   - Delega cálculo para a estratégia

4. **Client**: `SessionAnalytics`
   - Usa ScoreCalculator sem conhecer estratégia concreta
   - Prepara contexto com dados necessários
   - Integra pontuação com métricas de sessão

---

## Estrutura do Código

### Ficheiros Criados

```
strategies/
├── __init__.py                  # Exports do módulo
├── scoring_strategy.py          # Interface Strategy
├── time_based_scoring.py        # Estratégia: Tempo
├── accuracy_scoring.py          # Estratégia: Precisão
├── streak_scoring.py            # Estratégia: Streak
├── difficulty_scoring.py        # Estratégia: Dificuldade
├── composite_scoring.py         # Estratégia: Composta
└── score_calculator.py          # Context

session_module/
└── session_analytics.py         # MODIFICADO: Integração com Strategy

test_strategy_pattern.py         # Testes completos

Diagramas/Diagramas_Atividade6/
├── DiagramaComponentes_AtividadeCompleta.md
├── DiagramaSequencia_StrategyPattern.md
└── DiagramaEstrutura_StrategyPattern.md
```

### Integração com session_analytics.py

Modificações realizadas:
1. Import de estratégias e ScoreCalculator
2. Inicialização de `score_calculator` com CompositeScoringStrategy
3. Adição de campos: `current_streak`, `current_challenge_attempts`, `scores`, `total_score`
4. Método `log_challenge_complete()` agora:
   - Calcula pontuação usando Strategy
   - Atualiza streak automaticamente
   - Retorna resultado detalhado com breakdown
5. Exportação de métricas inclui: `totalScore`, `avgScore`, `bestStreak`

---

## Diagramas

### 1. Diagrama de Componentes - Sistema Completo
**Ficheiro:** `DiagramaComponentes_AtividadeCompleta.md`

Mostra a arquitetura completa integrando os 3 padrões:
- Factory Method (Criação) - Azul
- Decorator (Estrutural) - Laranja
- Strategy (Comportamental) - Verde

**Destaque:** Separação clara de responsabilidades entre padrões.

### 2. Diagrama de Sequência - Fluxo Completo
**Ficheiro:** `DiagramaSequencia_StrategyPattern.md`

Ilustra o fluxo completo de uma sessão:
1. Início de sessão
2. Criação de desafio (Factory)
3. Adição de funcionalidades (Decorator)
4. Resposta do aluno
5. **Cálculo de pontuação (Strategy)** ← NOVO
6. Atualização de streak e métricas
7. Fim de sessão
8. Export para Inven!RA

**Destaque:** Mostra como CompositeScoringStrategy combina múltiplas estratégias.

### 3. Diagrama de Estrutura - Strategy Pattern
**Ficheiro:** `DiagramaEstrutura_StrategyPattern.md`

Diagrama de classes UML detalhado mostrando:
- Interface ScoringStrategy
- 5 implementações concretas
- ScoreCalculator (Context)
- SessionAnalytics (Client)
- Relações entre componentes

**Inclui:** Fórmulas de cada estratégia e exemplos de uso.

---

## Como Testar

### Executar Testes Completos

```bash
python test_strategy_pattern.py
```

### O que é testado:

1. **Teste 1: TimeBasedScoringStrategy**
   - Resposta rápida (5s/30s) → 100 pontos
   - Resposta média (18s/30s) → 50 pontos
   - Timeout (31s/30s) → 0 pontos

2. **Teste 2: AccuracyScoringStrategy**
   - 1ª tentativa → 100 pontos
   - 2ª tentativa → 60 pontos
   - 3ª tentativa → 30 pontos
   - 4+ tentativas → 0 pontos

3. **Teste 3: StreakScoringStrategy**
   - Streak 0-1 → 50 pontos base
   - Streak 3 → 60 pontos (+10 bónus)
   - Streak 10 → 100 pontos (+50 bónus)

4. **Teste 4: DifficultyBasedScoringStrategy**
   - Dificuldade 1 (fácil) → 40 pontos
   - Dificuldade 3 (médio) → 80 pontos
   - Dificuldade 5 (difícil) → 100 pontos

5. **Teste 5: CompositeScoringStrategy**
   - Breakdown de pontuação ponderada
   - Exemplo: (75×0.4) + (100×0.4) + (60×0.2) = 82 pontos

6. **Teste 6: Strategy Switching**
   - Mesmo contexto, estratégias diferentes
   - Demonstra flexibilidade do padrão

7. **Teste 7: Integração com SessionAnalytics**
   - Fluxo completo de sessão
   - Tracking de streak e pontuação
   - Stats acumuladas do utilizador

### Output Esperado

```
============================================================
 TESTES DO STRATEGY PATTERN - SISTEMA DE PONTUACAO
 Atividade 6 - Padroes de Comportamento
============================================================

... [todos os testes passam] ...

============================================================
 TODOS OS TESTES CONCLUIDOS COM SUCESSO!
============================================================

>> O Strategy Pattern permite:
   [OK] Algoritmos de pontuacao intercambiaveis
   [OK] Facil extensao com novas estrategias
   [OK] Composicao de multiplas estrategias
   [OK] Troca de comportamento em runtime
   [OK] Codigo cliente desacoplado das implementacoes
```

---

## Integração com Padrões Anteriores

### Arquitetura Completa: 3 Padrões Trabalhando Juntos

```python
# 1. FACTORY METHOD (Atividade 4) - Criação
challenge = ChallengeFactory.create_challenge('visual', animal_id=2)

# 2. DECORATOR (Atividade 5) - Estrutura
timed_challenge = TimedDecorator(challenge, time_limit=30)

# 3. STRATEGY (Atividade 6) - Comportamento ← NOVO
session_id = session_analytics.start_session('student123')
session_analytics.log_challenge_start(session_id, timed_challenge)

# ... aluno responde ...

# Strategy calcula pontuação automaticamente
score_result = session_analytics.log_challenge_complete(
    session_id,
    timed_challenge.challenge_id,
    is_correct=True,
    difficulty=3,
    time_limit=30
)

print(score_result)
# {
#   'score': 82,
#   'performance': 'good',
#   'strategy': 'composite(time_based+accuracy_based+streak_based)',
#   'breakdown': {
#     'total_score': 82,
#     'components': [
#       {'strategy': 'time_based', 'score': 75, 'weight': 0.4, 'weighted_score': 30.0},
#       {'strategy': 'accuracy_based', 'score': 100, 'weight': 0.4, 'weighted_score': 40.0},
#       {'strategy': 'streak_based', 'score': 60, 'weight': 0.2, 'weighted_score': 12.0}
#     ]
#   }
# }
```

### Separação de Responsabilidades

| Padrão | Tipo | Responsabilidade | Atividade |
|--------|------|------------------|-----------|
| **Factory Method** | Criacional | **Criar** tipos de desafios | Atividade 4 |
| **Decorator** | Estrutural | **Estender** funcionalidades | Atividade 5 |
| **Strategy** | Comportamental | **Variar** algoritmo de pontuação | Atividade 6 |

Todos os três mantêm a interface `Challenge`, permitindo:
- **Polimorfismo**: Código cliente trabalha com interfaces
- **Composição**: Padrões podem ser combinados livremente
- **Extensibilidade**: Adicionar novos tipos, decorators ou estratégias sem modificar código existente

---

## Vantagens do Strategy Pattern

### Princípios SOLID Aplicados

1. **Single Responsibility Principle (SRP)**
   - Cada estratégia tem uma responsabilidade única
   - ScoreCalculator apenas delega cálculos

2. **Open/Closed Principle (OCP)**
   - Aberto para extensão: Novas estratégias sem modificar código
   - Fechado para modificação: Interface ScoringStrategy é estável

3. **Dependency Inversion Principle (DIP)**
   - SessionAnalytics depende da abstração (ScoringStrategy)
   - Não depende de implementações concretas

### Benefícios Práticos

✅ **Eliminação de Condicionais**
- Sem blocos `if/else` ou `switch` para escolher algoritmo
- Cada estratégia encapsula sua lógica

✅ **Runtime Flexibility**
- Trocar algoritmo em tempo de execução
- Configurável pela plataforma Inven!RA

✅ **Testabilidade**
- Cada estratégia testável independentemente
- Mock fácil para testes unitários

✅ **Reusabilidade**
- Estratégias podem ser reutilizadas em outros contextos
- CompositeScoringStrategy permite combinações

✅ **Extensibilidade**
- Adicionar nova estratégia = criar nova classe
- Zero impacto no código existente

---

## Exemplo: Adicionar Nova Estratégia

Suponha que queremos penalizar uso de dicas:

```python
# 1. Criar nova estratégia
from strategies.scoring_strategy import ScoringStrategy
from typing import Dict, Any

class HintPenaltyScoringStrategy(ScoringStrategy):
    def calculate_score(self, context: Dict[str, Any]) -> int:
        base_score = 100 if context.get('is_correct') else 0
        hints_used = context.get('hints_used', 0)
        penalty = hints_used * 15  # -15 pontos por dica
        return max(base_score - penalty, 0)

    def get_strategy_name(self) -> str:
        return "hint_penalty"

# 2. Usar imediatamente!
from session_module.session_analytics import session_analytics

session_analytics.score_calculator.set_strategy(
    HintPenaltyScoringStrategy()
)

# 3. Ou adicionar ao CompositeScoringStrategy
composite = CompositeScoringStrategy([
    (TimeBasedScoringStrategy(), 0.3),
    (AccuracyScoringStrategy(), 0.3),
    (HintPenaltyScoringStrategy(), 0.4)  # ← Nova estratégia
])
```

**Nenhuma modificação** em:
- SessionAnalytics
- ScoreCalculator
- Outras estratégias
- Código cliente

---

## Conclusão

O **Strategy Pattern** completa a tríade de padrões de design implementados no Activity Provider:

1. **Factory Method** cria os desafios
2. **Decorator** adiciona funcionalidades
3. **Strategy** define comportamento de pontuação

Esta arquitetura modular, extensível e testável demonstra a aplicação prática de:
- Padrões de design (GoF)
- Princípios SOLID
- Separation of Concerns
- Open/Closed Principle

O sistema resultante é **flexível, manutenível e preparado para evolução futura**, permitindo que a plataforma Inven!RA configure diferentes estratégias de pontuação conforme necessidades pedagógicas específicas.
