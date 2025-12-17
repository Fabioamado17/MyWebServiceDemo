# Módulo de Sessões - Fábio Amado

**Padrões Implementados:** Factory Method + Decorator
**Autores:** Henrique Crachat (2501450) & Fábio Amado (2501444)
**Objetivo:** Analytics de Sessões e Interações

---

## Visão Geral

Este módulo implementa dois padrões de design:
- **Factory Method (Criacional)**: Para criar desafios educativos
- **Decorator (Estrutural)**: Para adicionar funcionalidades aos desafios (tempo limite, dicas, etc.)

O módulo monitoriza padrões de sessão e interação dos alunos através de:

- Tempo de jogo por sessão
- Número de sessões realizadas
- Interações por desafio
- Dias consecutivos de jogo
- Duração média de sessão
- Tempo médio por desafio

---

## Integração com Factory Method

### Como o Módulo Usa o Padrão:

```python
from factories.challenge_factory import ChallengeFactory
from session_module.session_analytics import session_analytics

# 1. INICIAR sessão
session_id = session_analytics.start_session(user_id='student123')

# 2. CRIAR desafio usando Factory Method
challenge = ChallengeFactory.create_challenge('visual', animal_id=2)

# 3. LOG de início do desafio
session_analytics.log_challenge_start(session_id, challenge)

# 4. LOG de conclusão (tracking automático de tempo)
session_analytics.log_challenge_complete(
    session_id,
    challenge.challenge_id,
    is_correct=True
)

# 5. TERMINAR sessão
summary = session_analytics.end_session(session_id)
```

### Vantagens da Integração:

1. **Tracking Automático**: Tempo calculado automaticamente
2. **Desacoplamento**: Não precisa conhecer implementações concretas
3. **Polimorfismo**: Funciona com qualquer tipo de Challenge
4. **Métricas Ricas**: Tracking por tipo de desafio

---

## Padrão Decorator - TimedDecorator

### O que é o Padrão Decorator?

O padrão **Decorator** é um padrão estrutural que permite adicionar funcionalidades a objetos de forma dinâmica, sem modificar as classes base. É como "embrulhar" um objeto com funcionalidades extra.

### Problema Resolvido

No jogo "Dia & Noite", diferentes desafios podem precisar de funcionalidades adicionais:
- Limite de tempo
- Sistema de dicas
- Pontuação extra
- Dificuldade progressiva

Criar subclasses para todas as combinações seria impraticável:
- `AudioTimedChallenge`
- `AudioTimedScoredChallenge`
- `AudioTimedHintedScoredChallenge`
- ... (explosão combinatória!)

### Solução: Decorator Pattern

Com decorators, podemos combinar funcionalidades de forma modular:

```python
from factories.challenge_factory import ChallengeFactory
from decorators.timed_decorator import TimedDecorator

# 1. Criar desafio básico via Factory
base_challenge = ChallengeFactory.create_challenge('audio', animal_id=1)

# 2. "Embrulhar" com TimedDecorator para adicionar tempo limite
timed_challenge = TimedDecorator(base_challenge, time_limit=30)

# 3. Interface permanece igual (polimorfismo)
question = timed_challenge.get_question()
options = timed_challenge.get_options()

# 4. Mas agora tem funcionalidades extra!
timed_challenge.start_timer()
time_left = timed_challenge.get_time_remaining()
is_expired = timed_challenge.is_expired()
```

### TimedDecorator - Funcionalidades

O `TimedDecorator` adiciona as seguintes funcionalidades aos desafios:

| Funcionalidade | Descrição |
|----------------|-----------|
| **Limite de Tempo** | Define tempo máximo (em segundos) |
| **Cronometragem** | Rastreia início/fim automaticamente |
| **Tempo Restante** | Calcula quanto tempo falta |
| **Deteção de Timeout** | Verifica se tempo acabou |
| **Bónus de Velocidade** | 0-100 pontos baseado na rapidez |
| **Níveis de Performance** | 'excellent', 'good', 'fair', 'slow', 'timeout' |

### Exemplo Completo com TimedDecorator

```python
from factories.challenge_factory import ChallengeFactory
from decorators.timed_decorator import TimedDecorator
import time

# Criar desafio com limite de tempo
base = ChallengeFactory.create_challenge('visual', animal_id=2)
timed = TimedDecorator(base, time_limit=30)

# Iniciar cronómetro quando mostrar ao aluno
timed.start_timer()

# Mostrar pergunta e opções (interface igual ao Challenge normal)
print(timed.get_question())
print(timed.get_options())

# ... aluno a pensar (2 segundos) ...
time.sleep(2)

# Verificar tempo restante
print(f"Tempo restante: {timed.get_time_remaining():.1f}s")
print(f"Expirado? {timed.is_expired()}")

# Validar resposta (para cronómetro automaticamente)
is_correct = timed.validate_answer("Girafa")

# Calcular bónus baseado na velocidade
bonus = timed.calculate_time_bonus()  # 0-100 pontos
performance = timed.get_time_performance_level()  # 'excellent', 'good', etc.

print(f"Bónus: {bonus} pontos")
print(f"Performance: {performance}")
```

### Fórmula do Bónus de Tempo

O `TimedDecorator` calcula pontos bónus baseado na percentagem do tempo usado:

| Tempo Usado | Bónus | Exemplo (30s limite) |
|-------------|-------|----------------------|
| ≤ 25% | 100 pts | ≤ 7.5s |
| ≤ 50% | 50 pts | ≤ 15s |
| ≤ 75% | 25 pts | ≤ 22.5s |
| > 75% | 0 pts | > 22.5s |
| Timeout | 0 pts | ≥ 30s |

### Composição de Decorators

A grande vantagem: **decorators podem ser combinados** (stacked):

```python
# Criar desafio base
challenge = ChallengeFactory.create_challenge('habitat', animal_id=3)

# Adicionar múltiplas funcionalidades
challenge = TimedDecorator(challenge, time_limit=25)
challenge = HintDecorator(challenge, max_hints=3)  # Futuro
challenge = ScoredDecorator(challenge, points=100)  # Futuro

# Agora tem tempo + dicas + pontuação!
```

### Integração com Session Analytics

O módulo de sessões funciona transparentemente com desafios decorados:

```python
from session_module.session_analytics import session_analytics
from factories.challenge_factory import ChallengeFactory
from decorators.timed_decorator import TimedDecorator

# Iniciar sessão
session_id = session_analytics.start_session('student123')

# Criar desafio decorado
base = ChallengeFactory.create_challenge('audio', animal_id=1)
timed = TimedDecorator(base, time_limit=30)

# Log funciona igual (polimorfismo!)
session_analytics.log_challenge_start(session_id, timed)

# Iniciar cronómetro
timed.start_timer()

# ... aluno responde ...

# Validar e log
is_correct = timed.validate_answer(answer)
session_analytics.log_challenge_complete(session_id, timed.challenge_id, is_correct)

# Obter bónus e performance
bonus = timed.calculate_time_bonus()
performance = timed.get_time_performance_level()
```

### Cenário de Timeout

Se o tempo esgotar, a resposta não conta:

```python
timed = TimedDecorator(base, time_limit=2)
timed.start_timer()

# Aluno demora muito (3 segundos)
time.sleep(3)

# Verificar se expirou
if timed.is_expired():
    print("Tempo esgotado!")

# Tentar responder (mesmo corretamente, não conta!)
is_correct = timed.validate_answer(correct_answer)
print(is_correct)  # False (timeout!)

# Sem bónus
print(timed.calculate_time_bonus())  # 0
```

### Estrutura dos Decorators

```
decorators/
├── challenge_decorator.py    # Classe base abstrata
└── timed_decorator.py        # Decorator concreto (tempo)
```

**Criar Novos Decorators:**

```python
from decorators.challenge_decorator import ChallengeDecorator
from models.challenge import Challenge
from typing import Dict, Any

class HintDecorator(ChallengeDecorator):
    def __init__(self, challenge: Challenge, max_hints: int = 3):
        super().__init__(challenge)
        self.max_hints = max_hints
        self.hints_used = 0

    def get_hint(self) -> str:
        if self.hints_used < self.max_hints:
            self.hints_used += 1
            return self._generate_hint()
        return "Sem dicas disponíveis"

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data['hints_available'] = self.max_hints - self.hints_used
        return data
```

### Vantagens do Padrão Decorator

1. **Flexibilidade**: Adicionar/remover funcionalidades em runtime
2. **Composição**: Combinar múltiplos decorators
3. **Open/Closed Principle**: Estender sem modificar classes base
4. **Single Responsibility**: Cada decorator uma responsabilidade
5. **Reutilização**: Aplicar a qualquer tipo de Challenge
6. **Polimorfismo**: Interface `Challenge` mantida

### Factory + Decorator: Separação de Responsabilidades

| Padrão | Responsabilidade | Exemplo |
|--------|------------------|---------|
| **Factory Method** | **Criação** de tipos de desafios | `create_challenge('audio')` |
| **Decorator** | **Adicionar funcionalidades** | `TimedDecorator(challenge)` |

Ambos mantêm a interface `Challenge`, permitindo que o resto do sistema (session analytics, API) funcione sem conhecer os detalhes de implementação.

---

## Endpoints Implementados

### 1. Iniciar Sessão

```http
POST /api/session/start
Content-Type: application/json

{
  "user_id": "student123",
  "session_id": "optional_custom_id"
}
```

**Resposta:**
```json
{
  "success": true,
  "session_id": "student123_20241124120000",
  "message": "Sessão iniciada com sucesso"
}
```

### 2. Criar Desafio na Sessão

```http
POST /api/session/challenge
Content-Type: application/json

{
  "session_id": "student123_20241124120000",
  "animal_id": 1,
  "challenge_type": "audio"
}
```

**Resposta:**
```json
{
  "success": true,
  "challenge": {
    "challenge_id": "audio_1_4523",
    "type": "audio",
    "question": "Que animal produz este som?",
    "options": ["Leão", "Tigre", "Elefante", "Girafa"]
  },
  "session_context": {
    "challenges_in_session": 3,
    "interactions_in_session": 12,
    "session_duration": 125.5
  }
}
```

### 3. Concluir Desafio

```http
POST /api/session/complete-challenge
Content-Type: application/json

{
  "session_id": "student123_20241124120000",
  "challenge_id": "audio_1_4523",
  "is_correct": true
}
```

**Resposta:**
```json
{
  "success": true,
  "message": "Desafio concluído",
  "session_stats": {
    "challenges_attempted": 3,
    "avg_challenge_time": 18.3
  }
}
```

### 4. Registar Interação

```http
POST /api/session/interaction
Content-Type: application/json

{
  "session_id": "student123_20241124120000",
  "event_type": "click_hint",
  "event_data": {"element": "help_button"}
}
```

### 5. Terminar Sessão

```http
POST /api/session/end
Content-Type: application/json

{
  "session_id": "student123_20241124120000"
}
```

**Resposta:**
```json
{
  "success": true,
  "session_summary": {
    "session_id": "student123_20241124120000",
    "user_id": "student123",
    "duration": 245.8,
    "challenges_attempted": 5,
    "total_interactions": 23,
    "interaction_breakdown": {
      "challenge_start": 5,
      "challenge_complete": 5,
      "click_hint": 3
    },
    "avg_challenge_time": 22.5
  }
}
```

### 6. Ver Relatório de Sessões

```http
GET /api/session/report/student123
```

### 7. Ver Estatísticas do Utilizador

```http
GET /api/session/stats/student123
```

---

## Métricas Monitorizadas

### Por Sessão:

| Métrica | Descrição |
|---------|-----------|
| `session_id` | ID único da sessão |
| `duration` | Duração total em segundos |
| `challenges_attempted` | Desafios tentados |
| `total_interactions` | Total de interações |
| `interaction_breakdown` | Contagem por tipo |
| `avg_challenge_time` | Tempo médio por desafio |
| `challenge_times` | Tempos individuais |

### Por Utilizador (Agregado):

| Métrica | Descrição |
|---------|-----------|
| `total_sessions` | Total de sessões |
| `total_play_time` | Tempo total em segundos |
| `avg_session_time` | Duração média de sessão |
| `total_challenges` | Desafios totais |
| `total_interactions` | Interações totais |
| `consecutive_days` | Dias consecutivos jogando |

---

## Tracking Automático de Tempo

O módulo calcula automaticamente:

```python
# Tempo por desafio
log_challenge_start()     # Guarda timestamp início
# ... aluno responde ...
log_challenge_complete()  # Calcula duração automaticamente

# Duração da sessão
start_session()           # Guarda timestamp início
# ... aluno joga ...
end_session()            # Calcula duração total
```

---

## Dias Consecutivos

Lógica de contagem:

```python
Dia 1: Jogou → consecutive_days = 1
Dia 2: Jogou → consecutive_days = 2
Dia 3: Não jogou
Dia 4: Jogou → consecutive_days = 1 (reset)
```

---

## Integração com Inven!RA

```http
POST /api/analytics
Content-Type: application/json

{
  "studentId": "student123"
}
```

**Formato de Resposta (Compatível Inven!RA):**
```json
{
  "success": true,
  "analytics": {
    "studentId": "student123",
    "activityId": "dia-noite-animals",
    "sessionMetrics": {
      "totalSessions": 12,
      "totalPlayTime": 3456.7,
      "totalChallenges": 58,
      "totalInteractions": 234,
      "consecutiveDays": 5,
      "avgSessionTime": 288.1
    },
    "timestamp": "2024-11-24T12:30:00"
  }
}
```

---

## Exemplo de Uso Completo

```python
from factories.challenge_factory import ChallengeFactory
from session_module.session_analytics import session_analytics

# Fluxo completo de uma sessão
user_id = "student123"

# 1. Iniciar sessão
session_id = session_analytics.start_session(user_id)

# 2. Loop de desafios
for i in range(3):
    # Criar desafio
    challenge = ChallengeFactory.create_random_challenge(animal_id=i+1)
    
    # Log início
    session_analytics.log_challenge_start(session_id, challenge)
    
    # ... aluno responde ...
    
    # Log conclusão
    session_analytics.log_challenge_complete(
        session_id,
        challenge.challenge_id,
        is_correct=True
    )
    
    # Log interações adicionais
    session_analytics.log_interaction(
        session_id,
        'click_next',
        {'button': 'next_challenge'}
    )

# 3. Terminar sessão
summary = session_analytics.end_session(session_id)

print(f"Duração: {summary['duration']}s")
print(f"Desafios: {summary['challenges_attempted']}")
print(f"Tempo médio: {summary['avg_challenge_time']}s")
```

---

## Tipos de Interações Tracked

| Tipo | Descrição | Exemplo |
|------|-----------|---------|
| `challenge_start` | Início de desafio | Auto |
| `challenge_complete` | Conclusão de desafio | Auto |
| `click_hint` | Clique em dica | Manual |
| `click_audio` | Reproduzir áudio | Manual |
| `hover_option` | Hover sobre opção | Manual |
| `navigation` | Navegação | Manual |
| `submit_answer` | Submeter resposta | Manual |

---

## Integração no App.py

```python
from session_module.session_endpoints import register_session_routes

# No App.py, após criar app
register_session_routes(app)
```

---

## Testar o Sistema

### Testar Factory Method

```bash
python test_factory.py
```

Testa a criação de desafios via `ChallengeFactory`:
- Criação de tipos específicos (`audio`, `visual`, `habitat`, `classification`)
- Criação aleatória
- Criação de conjuntos completos

### Testar Decorator Pattern

```bash
python test_timed_decorator.py
```

Demonstra o padrão Decorator com `TimedDecorator`:
- Desafios com limite de tempo
- Cenários de timeout
- Níveis de performance (excellent, good, fair, slow, timeout)
- Polimorfismo (interface mantida)
- Reset e retry
- Cálculo de bónus de tempo

**Output esperado:**
```
========================================
 TESTE 1: Desafio com Limite de Tempo
========================================

Desafio base criado: AudioChallenge(...)
Desafio decorado: TimedDecorator(...)
  - Limite de tempo: 30s

Cronómetro iniciado!

Pergunta: Que animal produz este som?
Opções: ['Leão', 'Tigre', ...]

Tempo decorrido: 2.00s
Tempo restante: 28.00s
Expirado? False

Resposta validada: Correto!
Bónus de tempo: 100 pontos
Performance: excellent
```

### Testar API Endpoints

```bash
python test_api.py
```

Testa todos os endpoints REST:
- Endpoints Inven!RA (`/api/params`, `/api/deploy`, `/api/analytics`)
- Endpoints de Sessão (`/api/session/*`)

---

## Relatório de Sessões

```python
report = session_analytics.get_user_sessions_report('student123')

# Estrutura:
{
  'user_id': 'student123',
  'total_sessions': 12,
  'total_play_time': 3456.7,
  'avg_session_time': 288.1,
  'total_challenges': 58,
  'total_interactions': 234,
  'consecutive_days': 5,
  'sessions': [
    {
      'session_id': '...',
      'duration': 245.8,
      'challenges_attempted': 5,
      ...
    },
    ...
  ]
}
```

---

## Resumo dos Padrões Implementados

### Arquitetura Completa

```
┌─────────────────────────────────────────────────────────────┐
│                    FACTORY METHOD PATTERN                   │
│                     (Criational Pattern)                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ChallengeFactory.create_challenge('audio', animal_id=1)   │
│            ↓                                                │
│    AudioChallenge / VisualChallenge / HabitatChallenge     │
│            ↓                                                │
│       [Base Challenge Object]                               │
│                                                             │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ↓
┌─────────────────────────────────────────────────────────────┐
│                    DECORATOR PATTERN                         │
│                   (Structural Pattern)                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  TimedDecorator(base_challenge, time_limit=30)             │
│            ↓                                                │
│    [Enhanced Challenge with Timing Features]               │
│    - start_timer()                                          │
│    - get_time_remaining()                                   │
│    - calculate_time_bonus()                                 │
│    - is_expired()                                           │
│                                                             │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ↓
┌─────────────────────────────────────────────────────────────┐
│                   SESSION ANALYTICS                         │
│                  (Singleton Pattern)                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  session_analytics.log_challenge_start(session_id, challenge)│
│  session_analytics.log_challenge_complete(...)              │
│            ↓                                                │
│  Tracks timing, interactions, performance                   │
│            ↓                                                │
│  Export to Inven!RA format                                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Fluxo Completo: Factory + Decorator + Session

```python
# 1. FACTORY METHOD: Criar desafio
challenge = ChallengeFactory.create_challenge('visual', animal_id=2)

# 2. DECORATOR: Adicionar funcionalidades
timed_challenge = TimedDecorator(challenge, time_limit=30)

# 3. SESSION ANALYTICS: Tracking
session_id = session_analytics.start_session('student123')
session_analytics.log_challenge_start(session_id, timed_challenge)

# 4. TIMING: Cronometrar
timed_challenge.start_timer()

# 5. APRESENTAR ao aluno
print(timed_challenge.get_question())
print(timed_challenge.get_options())
print(f"Tempo: {timed_challenge.get_time_remaining():.0f}s")

# 6. VALIDAR resposta
is_correct = timed_challenge.validate_answer(student_answer)

# 7. MÉTRICAS
bonus = timed_challenge.calculate_time_bonus()
performance = timed_challenge.get_time_performance_level()

# 8. LOG conclusão
session_analytics.log_challenge_complete(
    session_id,
    timed_challenge.challenge_id,
    is_correct
)

# 9. TERMINAR sessão
summary = session_analytics.end_session(session_id)

# 10. EXPORT para Inven!RA
analytics = session_analytics.export_analytics('student123')
```

### Benefícios da Arquitetura

| Aspeto | Benefício |
|--------|-----------|
| **Separação de Responsabilidades** | Factory cria, Decorator aumenta, Session rastreia |
| **Flexibilidade** | Adicionar novos tipos de desafios ou decorators sem modificar código existente |
| **Testabilidade** | Cada componente pode ser testado independentemente |
| **Manutenibilidade** | Código organizado por responsabilidade (SRP - Single Responsibility Principle) |
| **Extensibilidade** | Fácil adicionar novos decorators (hints, scoring, difficulty) |
| **Polimorfismo** | Toda a API funciona com interface `Challenge` base |

### Padrões Futuros (Sugestões)

Outros decorators que poderiam ser implementados:

- **ScoredDecorator**: Sistema de pontuação baseado em dificuldade
- **HintDecorator**: Sistema de dicas progressivas
- **DifficultyDecorator**: Ajuste dinâmico de dificuldade
- **AchievementDecorator**: Conquistas e badges
- **DetailedAnalyticsDecorator**: Métricas extra (movimentos do rato, padrões de clique)

---

## Autores

**Henrique Crachat** (2501450@estudante.uab.pt)
- Factory Method Pattern
- Challenge types (Audio, Visual, Habitat, Classification)
- Cognitive Module

**Fábio Amado** (2501444@estudante.uab.pt)
- Decorator Pattern (TimedDecorator)
- Session Analytics Module
- Integration with Inven!RA

**Universidade Aberta**
UC: Arquitetura e Padrões de Software
