"""
Decorators de Validação - Refatoração Cut-and-Paste Programming.

Este módulo elimina a duplicação de código de validação nos endpoints,
centralizando a lógica em decorators reutilizáveis.

ANTIPADRÃO RESOLVIDO: Cut-and-Paste Programming
- Antes: Código de validação repetido em 7+ endpoints
- Depois: Decorator único @validate_request aplicado em cada endpoint

Autor: Fábio Amado (2501444)
"""
from functools import wraps
from flask import request, jsonify
from typing import Type, Optional
import logging

logger = logging.getLogger(__name__)


def validate_json(f):
    """
    Decorator básico que valida se o request contém JSON válido.

    Uso:
        @app.route("/api/endpoint", methods=['POST'])
        @validate_json
        def endpoint():
            data = request.get_json()
            # data garantidamente não é None
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        data = request.get_json()

        if data is None:
            return jsonify({
                'success': False,
                'error': 'Corpo da requisição deve ser JSON válido'
            }), 400

        return f(*args, **kwargs)

    return wrapper


def validate_request(schema_class: Type):
    """
    Decorator para validação robusta de requests usando schemas.

    RESOLVE: Cut-and-Paste Programming + Input Kludge

    Este decorator:
    1. Verifica se o corpo é JSON válido
    2. Instancia o schema com os dados
    3. Executa validação completa (tipos, formatos, valores)
    4. Passa dados validados para a função

    Args:
        schema_class: Classe de schema para validação (ex: ChallengeRequest)

    Uso:
        @app.route("/api/session/challenge", methods=['POST'])
        @validate_request(ChallengeRequest)
        def session_challenge(validated_data):
            # validated_data é instância de ChallengeRequest já validada
            # Acesso seguro: validated_data.session_id, validated_data.animal_id

    Benefícios:
    - Validação centralizada (DRY)
    - Erros claros e consistentes
    - Tipos garantidos
    - Código do endpoint focado na lógica de negócio
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # 1. Verificar se há JSON
            data = request.get_json()

            if data is None:
                logger.warning(f"Request sem JSON para {f.__name__}")
                return jsonify({
                    'success': False,
                    'error': 'Corpo da requisição deve ser JSON válido'
                }), 400

            # 2. Tentar criar e validar schema
            try:
                validated = schema_class.from_dict(data)
                validated.validate()

            except ValueError as e:
                logger.warning(f"Validação falhou em {f.__name__}: {str(e)}")
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 400

            except TypeError as e:
                logger.warning(f"Campos inválidos em {f.__name__}: {str(e)}")
                return jsonify({
                    'success': False,
                    'error': f'Campos inválidos: {str(e)}'
                }), 400

            # 3. Passar dados validados para a função
            return f(validated, *args, **kwargs)

        return wrapper
    return decorator


def handle_endpoint_errors(f):
    """
    Decorator para tratamento centralizado de erros em endpoints.

    RESOLVE: Cut-and-Paste Programming (blocos try-except repetidos)

    Uso:
        @app.route("/api/endpoint", methods=['POST'])
        @handle_endpoint_errors
        def endpoint():
            # Código sem try-except
            # Exceções são tratadas automaticamente
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)

        except ValueError as e:
            logger.error(f"ValueError em {f.__name__}: {str(e)}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 400

        except KeyError as e:
            logger.error(f"KeyError em {f.__name__}: {str(e)}")
            return jsonify({
                'success': False,
                'error': f'Campo não encontrado: {str(e)}'
            }), 400

        except Exception as e:
            logger.exception(f"Erro inesperado em {f.__name__}: {str(e)}")
            return jsonify({
                'success': False,
                'error': 'Erro interno do servidor'
            }), 500

    return wrapper
