# backend/run.py
from app import create_app
from app.services.rag_service import rag_service
import click

app = create_app()

@app.cli.command("index")
def index_data():
    print("CLI: Starting index process...")
    try:
        rag_service.index_redmine_data()
        print("CLI: Index process finished.")
    except Exception as e:
        print(f"CLI: Indexing error: {e}")