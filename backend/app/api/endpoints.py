# backend/app/api/endpoints.py

import traceback
from flask import Blueprint, request, jsonify
from app.services.rag_service import rag_service

# 1. Criação do Blueprint para agrupar as rotas da nossa API
#    O 'url_prefix' adiciona /api antes de todas as rotas deste blueprint.
#    Ex: /ask vira /api/ask
api_bp = Blueprint('api', __name__, url_prefix='/api')


# 2. Definição da Rota /ask
@api_bp.route('/ask', methods=['POST'])
def ask():
    """
    Recebe uma pergunta em formato JSON, passa para o serviço de RAG
    e retorna a resposta.
    """
    # Validação de entrada
    if not request.is_json:
        return jsonify({"error": "Missing JSON in request"}), 400

    data = request.get_json()
    if 'question' not in data:
        return jsonify({"error": "Missing 'question' field in request"}), 400

    # Bloco de execução com depuração detalhada
    try:
        question = data['question']
        answer = rag_service.ask_question(question)
        return jsonify({"answer": answer})

    except Exception as e:
        # ---- INÍCIO DO BLOCO DE DEBUG ----
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("!!!!!!!!! ERRO CAPTURADO NO ENDPOINT /ask !!!!!!!!!!")
        # Imprime o stack trace completo e detalhado no log do contêiner
        traceback.print_exc()
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        # ---- FIM DO BLOCO DE DEBUG ----
        return jsonify({"error": "An internal error occurred", "details": str(e)}), 500


# 3. Definição da Rota /index
@api_bp.route('/index', methods=['POST'])
def index():
    """
    Dispara o processo de re-indexação dos dados do Redmine.
    Não recebe corpo na requisição.
    """
    try:
        # Delega a tarefa de indexação para o nosso serviço
        rag_service.index_redmine_data()
        return jsonify({"status": "Indexing process started successfully"}), 200

    except Exception as e:
        print(f"ERROR in /index endpoint: {e}")
        return jsonify({"error": "Failed to start indexing process"}), 500