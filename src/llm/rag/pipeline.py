from src.llm.rag.rag_agent.agent import RagAgent
from src.llm.rag.injection.ingest import ingest_documents
import warnings

warnings.filterwarnings("ignore", category=ResourceWarning)

def rag_model(chat_history,user_input):
    
    agent = RagAgent()
    try:
        response  = agent.run(
            chat_history=chat_history, user_message=user_input
        )
        return response

    except Exception as e:
        print(f"\n Error: {e}\n")

def run_injection():
    ingest_documents()