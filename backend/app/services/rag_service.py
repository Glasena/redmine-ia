from redminelib import Redmine
import chromadb
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.docstore.document import Document
from langchain_community.vectorstores import Chroma

from app.config import REDMINE_URL, REDMINE_KEY, CHROMA_HOST

class RAGService:
    def __init__(self):
        print("Starting RAG Service...")
        # 1. Conecta ao servidor ChromaDB
        self.client = chromadb.HttpClient(host=CHROMA_HOST, port=8000)
        
        # 2. Prepara o "tradutor" de texto para vetores
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        
        # 3. Prepara o "cérebro" (Gemini)
        self.llm = ChatGoogleGenerativeAI(model="models/gemini-1.5-pro-latest", temperature=0.2)
        
        # 4. Aponta o LangChain para nossa "memória" no ChromaDB
        self.vector_store = Chroma(
            client=self.client,
            collection_name="redmine_collection",
            embedding_function=self.embeddings,
        )
        
        # 5. Monta a "máquina de responder perguntas" (RetrievalQA Chain)
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever()
        )
        print("RAG Service initialized.")

    def index_redmine_data(self):
        print("Iniciando a indexação dos dados do Redmine...")
        try:
            redmine = Redmine(REDMINE_URL, key=REDMINE_KEY)
            projetos = redmine.project.all()
            documentos = []
            for projeto in projetos:
                tarefas = redmine.issue.filter(project_id=projeto.id, status_id='*')
                for tarefa in tarefas:
                    conteudo = f"Projeto: {projeto.name}\nID: {tarefa.id}\nTítulo: {tarefa.subject}\nStatus: {tarefa.status.name}\nDescrição: {getattr(tarefa, 'description', 'N/A')}"
                    documentos.append(Document(page_content=conteudo))
            
            if documentos:
                self.vector_store.add_documents(documentos)
                print(f"Indexação concluída. {len(documentos)} documentos processados.")
            else:
                print("Nenhum documento encontrado para indexar.")
        except Exception as e:
            print(f"Erro durante a indexação: {e}")
            raise

    def ask_question(self, query):
        print(f"Question recieved: {query}")
        # O método invoke é o padrão mais recente do LangChain
        response = self.qa_chain.invoke({"query": query})
        return response['result']

# Instancia o serviço para ser usado na aplicação (padrão Singleton)
rag_service = RAGService()