"""
Endpoints Flask para Módulo de Sessões - Fábio Amado (2501444)

Integra Factory Method (ChallengeFactory) com Session Analytics.

Autor: Fábio Amado (2501444@estudante.uab.pt)
"""
from flask import request, jsonify
from factories.challenge_factory import ChallengeFactory
from session_module.session_analytics import session_analytics


# =====================================================
# ENDPOINTS DO MÓDULO SESSÕES (FÁBIO)
# =====================================================
# Adicionar estas rotas ao App.py existente
# =====================================================


def register_session_routes(app):
    """
    Registar rotas do módulo de sessões no Flask app.
    
    Args:
        app: Instância Flask
    """
    
    @app.route("/api/session/start", methods=['POST'])
    def start_session():
        """
        Inicia uma nova sessão de jogo.
        
        Body:
        {
            "user_id": "student123",
            "session_id": "optional_custom_id"
        }
        
        Returns:
            ID da sessão criada
        """
        data = request.get_json()
        
        if not data or 'user_id' not in data:
            return jsonify({
                'success': False,
                'error': 'user_id é obrigatório'
            }), 400
        
        try:
            session_id = session_analytics.start_session(
                data['user_id'],
                data.get('session_id')
            )
            
            return jsonify({
                'success': True,
                'session_id': session_id,
                'message': 'Sessão iniciada com sucesso'
            })
        
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    
    @app.route("/api/session/challenge", methods=['POST'])
    def session_challenge():
        """
        Cria desafio dentro de uma sessão com tracking.
        
        INTEGRAÇÃO FACTORY METHOD:
        - Usa ChallengeFactory.create_challenge()
        - Log automático em session_analytics
        
        Body:
        {
            "session_id": "student123_20241124120000",
            "animal_id": 1,
            "challenge_type": "audio"
        }
        
        Returns:
            Challenge + dados de sessão
        """
        data = request.get_json()
        
        required = ['session_id', 'animal_id']
        if not all(field in data for field in required):
            return jsonify({
                'success': False,
                'error': f'Campos obrigatórios: {required}'
            }), 400
        
        try:
            # USAR FACTORY METHOD para criar desafio
            challenge_type = data.get('challenge_type', 'random')
            
            if challenge_type == 'random':
                challenge = ChallengeFactory.create_random_challenge(
                    data['animal_id']
                )
            else:
                challenge = ChallengeFactory.create_challenge(
                    challenge_type,
                    data['animal_id']
                )
            
            # LOG de início do desafio na sessão
            session_analytics.log_challenge_start(
                data['session_id'],
                challenge
            )
            
            # Obter dados da sessão atual
            session_summary = session_analytics.get_session_summary(
                data['session_id']
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
        
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    
    @app.route("/api/session/complete-challenge", methods=['POST'])
    def complete_challenge():
        """
        Regista conclusão de desafio com tracking de tempo.
        
        Body:
        {
            "session_id": "student123_20241124120000",
            "challenge_id": "audio_1_4523",
            "is_correct": true
        }
        
        Returns:
            Confirmação + stats da sessão
        """
        data = request.get_json()
        
        required = ['session_id', 'challenge_id', 'is_correct']
        if not all(field in data for field in required):
            return jsonify({
                'success': False,
                'error': f'Campos obrigatórios: {required}'
            }), 400
        
        try:
            session_analytics.log_challenge_complete(
                data['session_id'],
                data['challenge_id'],
                data['is_correct']
            )
            
            session_summary = session_analytics.get_session_summary(
                data['session_id']
            )
            
            return jsonify({
                'success': True,
                'message': 'Desafio concluído',
                'session_stats': {
                    'challenges_attempted': session_summary['challenges_attempted'],
                    'avg_challenge_time': session_summary['avg_challenge_time']
                }
            })
        
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    
    @app.route("/api/session/interaction", methods=['POST'])
    def log_interaction():
        """
        Regista interação genérica do aluno.
        
        Body:
        {
            "session_id": "student123_20241124120000",
            "event_type": "click_hint",
            "event_data": {"element": "help_button"}
        }
        
        Returns:
            Confirmação
        """
        data = request.get_json()
        
        if not data or 'session_id' not in data or 'event_type' not in data:
            return jsonify({
                'success': False,
                'error': 'session_id e event_type são obrigatórios'
            }), 400
        
        try:
            session_analytics.log_interaction(
                data['session_id'],
                data['event_type'],
                data.get('event_data')
            )
            
            return jsonify({
                'success': True,
                'message': 'Interação registada'
            })
        
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    
    @app.route("/api/session/end", methods=['POST'])
    def end_session():
        """
        Termina sessão e retorna sumário completo.
        
        Body:
        {
            "session_id": "student123_20241124120000"
        }
        
        Returns:
            Sumário completo da sessão
        """
        data = request.get_json()
        
        if not data or 'session_id' not in data:
            return jsonify({
                'success': False,
                'error': 'session_id é obrigatório'
            }), 400
        
        try:
            summary = session_analytics.end_session(data['session_id'])
            
            return jsonify({
                'success': True,
                'session_summary': summary
            })
        
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    
    @app.route("/api/session/report/<user_id>", methods=['GET'])
    def get_session_report(user_id):
        """
        Retorna relatório de todas as sessões de um utilizador.
        
        Example:
            GET /api/session/report/student123
        """
        try:
            report = session_analytics.get_user_sessions_report(user_id)
            
            return jsonify({
                'success': True,
                'report': report
            })
        
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    
    @app.route("/api/analytics", methods=['POST'])
    def get_session_analytics():
        """
        Endpoint compatível com Inven!RA para analytics de sessão.
        
        Body:
        {
            "studentId": "student123"
        }
        
        Returns:
            Analytics formatados para Inven!RA
        """
        data = request.get_json()
        
        if not data or 'studentId' not in data:
            return jsonify({
                'success': False,
                'error': 'studentId é obrigatório'
            }), 400
        
        try:
            analytics = session_analytics.export_analytics(data['studentId'])
            
            return jsonify({
                'success': True,
                'analytics': analytics
            })
        
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    
    @app.route("/api/session/stats/<user_id>", methods=['GET'])
    def get_user_stats(user_id):
        """
        Retorna estatísticas agregadas de um utilizador.
        
        Example:
            GET /api/session/stats/student123
        """
        try:
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
        
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500


# =====================================================
# INSTRUÇÕES DE INTEGRAÇÃO
# =====================================================
"""
Para integrar no App.py:

1. Importar no início:
   from session_module.session_endpoints import register_session_routes

2. Depois de criar app, adicionar:
   register_session_routes(app)

3. Testar endpoints:
   
   # Iniciar sessão
   curl -X POST http://localhost:5000/api/session/start \
     -H "Content-Type: application/json" \
     -d '{"user_id": "student123"}'
   
   # Criar desafio na sessão
   curl -X POST http://localhost:5000/api/session/challenge \
     -H "Content-Type: application/json" \
     -d '{"session_id": "student123_20241124120000", "animal_id": 1, "challenge_type": "audio"}'
   
   # Concluir desafio
   curl -X POST http://localhost:5000/api/session/complete-challenge \
     -H "Content-Type: application/json" \
     -d '{"session_id": "student123_20241124120000", "challenge_id": "audio_1_4523", "is_correct": true}'
   
   # Terminar sessão
   curl -X POST http://localhost:5000/api/session/end \
     -H "Content-Type: application/json" \
     -d '{"session_id": "student123_20241124120000"}'
   
   # Ver relatório
   curl http://localhost:5000/api/session/report/student123
"""
