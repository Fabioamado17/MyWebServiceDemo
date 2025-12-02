# Módulo de Sessões - Fábio Amado

**Padrão Implementado:** Factory Method  
**Autor:** Fábio Amado (2501444@estudante.uab.pt)  
**Objetivo:** Analytics de Sessões e Interações

---

## Visão Geral

Este módulo usa o padrão Factory Method (ChallengeFactory) para criar desafios educativos e monitoriza padrões de sessão e interação dos alunos através de:

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
