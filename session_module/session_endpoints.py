"""
Endpoints Flask para Módulo de Sessões - Refatorado.

REFATORAÇÕES APLICADAS:
1. Cut-and-Paste Programming → Decorator @validate_request centraliza validação
2. Input Kludge → Schemas validam tipos, formatos e valores

Autor: Fábio Amado (2501444@estudante.uab.pt)
"""
from flask import request, jsonify
from factories.challenge_factory import ChallengeFactory
from session_module.session_analytics import session_analytics
from validation.decorators import validate_request, handle_endpoint_errors
from validation.schemas import (
    SessionStartRequest,
    ChallengeRequest,
    ChallengeCompleteRequest,
    InteractionRequest,
    SessionEndRequest,
    AnalyticsRequest
)


def register_session_routes(app):
    """
    Registar rotas do módulo de sessões no Flask app.

    NOTA: Endpoints refatorados para usar:
    - @validate_request(Schema) - Validação automática
    - @handle_endpoint_errors - Tratamento de erros centralizado

    Args:
        app: Instância Flask
    """

    @app.route("/api/session/start", methods=['POST'])
    @validate_request(SessionStartRequest)
    @handle_endpoint_errors
    def start_session(validated: SessionStartRequest):
        """
        Inicia uma nova sessão de jogo.

        Body:
        {
            "user_id": "student123",
            "session_id": "optional_custom_id"  // opcional
        }

        Returns:
            ID da sessão criada
        """
        session_id = session_analytics.start_session(
            validated.user_id,
            validated.session_id
        )

        return jsonify({
            'success': True,
            'session_id': session_id,
            'message': 'Sessão iniciada com sucesso'
        })


    @app.route("/api/session/challenge", methods=['POST'])
    @validate_request(ChallengeRequest)
    @handle_endpoint_errors
    def session_challenge(validated: ChallengeRequest):
        """
        Cria desafio dentro de uma sessão com tracking.

        INTEGRAÇÃO FACTORY METHOD:
        - Usa ChallengeFactory.create_challenge()
        - Log automático em session_analytics

        Body:
        {
            "session_id": "student123_20241124120000",
            "animal_id": 1,                    // inteiro, animal existente
            "challenge_type": "audio",         // opcional, default: "random"
            "difficulty": 1                    // opcional, 1-5, default: 1
        }

        Returns:
            Challenge + dados de sessão
        """
        # Validação adicional: sessão existe e está ativa
        validated.validate_session_exists(session_analytics)

        # USAR FACTORY METHOD para criar desafio
        if validated.challenge_type == 'random':
            challenge = ChallengeFactory.create_random_challenge(
                validated.animal_id,
                validated.difficulty
            )
        else:
            challenge = ChallengeFactory.create_challenge(
                validated.challenge_type,
                validated.animal_id,
                validated.difficulty
            )

        # LOG de início do desafio na sessão
        session_analytics.log_challenge_start(
            validated.session_id,
            challenge
        )

        # Obter dados da sessão atual
        session_summary = session_analytics.get_session_summary(
            validated.session_id
        )

        return jsonify({
            'success': True,
            'challenge': challenge.to_dict(),
            'session_context': {
                'challenges_in_session': session_summary['challenges_attempted'],
                'interactions_in_session': session_summary['total_interactions'],
                'session_duration': session_summary['duration']
            }
        })


    @app.route("/api/session/complete-challenge", methods=['POST'])
    @validate_request(ChallengeCompleteRequest)
    @handle_endpoint_errors
    def complete_challenge(validated: ChallengeCompleteRequest):
        """
        Regista conclusão de desafio com tracking de tempo.

        Body:
        {
            "session_id": "student123_20241124120000",
            "challenge_id": "audio_1_4523",
            "is_correct": true,               // DEVE ser booleano
            "difficulty": 3,                  // opcional, 1-5
            "time_limit": 30                  // opcional, segundos
        }

        Returns:
            Confirmação + stats da sessão + pontuação
        """
        # Validação adicional: desafio foi iniciado na sessão
        validated.validate_challenge_started(session_analytics)

        score_result = session_analytics.log_challenge_complete(
            validated.session_id,
            validated.challenge_id,
            validated.is_correct,
            validated.difficulty,
            validated.time_limit
        )

        session_summary = session_analytics.get_session_summary(
            validated.session_id
        )

        return jsonify({
            'success': True,
            'message': 'Desafio concluído',
            'score': score_result,
            'session_stats': {
                'challenges_attempted': session_summary['challenges_attempted'],
                'avg_challenge_time': session_summary['avg_challenge_time'],
                'total_score': session_summary['total_score'],
                'current_streak': session_summary['current_streak']
            }
        })


    @app.route("/api/session/interaction", methods=['POST'])
    @validate_request(InteractionRequest)
    @handle_endpoint_errors
    def log_interaction(validated: InteractionRequest):
        """
        Regista interação genérica do aluno.

        Body:
        {
            "session_id": "student123_20241124120000",
            "event_type": "click_hint",
            "event_data": {"element": "help_button"}  // opcional
        }

        Returns:
            Confirmação
        """
        session_analytics.log_interaction(
            validated.session_id,
            validated.event_type,
            validated.event_data
        )

        return jsonify({
            'success': True,
            'message': 'Interação registada'
        })


    @app.route("/api/session/end", methods=['POST'])
    @validate_request(SessionEndRequest)
    @handle_endpoint_errors
    def end_session(validated: SessionEndRequest):
        """
        Termina sessão e retorna sumário completo.

        Body:
        {
            "session_id": "student123_20241124120000"
        }

        Returns:
            Sumário completo da sessão
        """
        summary = session_analytics.end_session(validated.session_id)

        return jsonify({
            'success': True,
            'session_summary': summary
        })


    @app.route("/api/session/report/<user_id>", methods=['GET'])
    @handle_endpoint_errors
    def get_session_report(user_id):
        """
        Retorna relatório de todas as sessões de um utilizador.

        Example:
            GET /api/session/report/student123
        """
        # Validação simples para GET
        if not user_id or not isinstance(user_id, str):
            return jsonify({
                'success': False,
                'error': 'user_id inválido'
            }), 400

        report = session_analytics.get_user_sessions_report(user_id)

        return jsonify({
            'success': True,
            'report': report
        })


    @app.route("/api/analytics", methods=['POST'])
    @validate_request(AnalyticsRequest)
    @handle_endpoint_errors
    def get_session_analytics(validated: AnalyticsRequest):
        """
        Endpoint compatível com Inven!RA para analytics de sessão.

        Body:
        {
            "studentId": "student123"
        }

        Returns:
            Analytics formatados para Inven!RA
        """
        analytics = session_analytics.export_analytics(validated.student_id)

        return jsonify({
            'success': True,
            'analytics': analytics
        })


    @app.route("/api/session/stats/<user_id>", methods=['GET'])
    @handle_endpoint_errors
    def get_user_stats(user_id):
        """
        Retorna estatísticas agregadas de um utilizador.

        Example:
            GET /api/session/stats/student123
        """
        # Validação simples para GET
        if not user_id or not isinstance(user_id, str):
            return jsonify({
                'success': False,
                'error': 'user_id inválido'
            }), 400

        if user_id not in session_analytics.user_stats:
            return jsonify({
                'success': False,
                'error': 'Utilizador não encontrado'
            }), 404

        stats = session_analytics.user_stats[user_id]

        return jsonify({
            'success': True,
            'user_id': user_id,
            'stats': stats
        })


# =====================================================
# DOCUMENTAÇÃO DA REFATORAÇÃO
# =====================================================
"""
ANTIPADRÕES RESOLVIDOS:

1. CUT-AND-PASTE PROGRAMMING
   Antes: Cada endpoint tinha código de validação similar:

   data = request.get_json()
   if not data or 'field' not in data:
       return jsonify({'success': False, 'error': '...'}), 400
   try:
       ...
   except Exception as e:
       return jsonify({'success': False, 'error': str(e)}), 500

   Depois: Decorator @validate_request elimina duplicação:

   @validate_request(Schema)
   @handle_endpoint_errors
   def endpoint(validated):
       # Código focado na lógica de negócio

2. INPUT KLUDGE
   Antes: Validação apenas de presença:

   if not all(field in data for field in required):
       return error
   # Não validava tipos, formatos, ou valores!

   Depois: Schemas validam completamente:

   - Tipos (string, int, bool)
   - Formatos (não vazio, comprimento máximo)
   - Valores (ranges, existência de recursos)
   - Mensagens de erro claras e específicas

BENEFÍCIOS:
- ~137 linhas de código duplicado eliminadas
- Validação consistente em todos os endpoints
- Erros claros indicam exatamente o problema
- Código dos endpoints focado na lógica de negócio
- Fácil adicionar novos endpoints com validação
- Testabilidade: schemas testáveis isoladamente
"""
