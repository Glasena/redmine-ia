# backend/app/__init__.py

from flask import Flask

def create_app():
    """
    Esta é a Application Factory. Ela constrói e configura a aplicação Flask.
    """
    # 1. Cria a instância principal da aplicação Flask
    # __name__ ajuda o Flask a saber onde encontrar arquivos de template e estáticos.
    app = Flask(__name__)

    # 2. Importa e registra as rotas (Blueprint) da nossa API
    # A importação é feita AQUI DENTRO para evitar importações circulares.
    from .api.endpoints import api_bp
    app.register_blueprint(api_bp)

    # 3. Retorna a aplicação final, montada e configurada
    return app