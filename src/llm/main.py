from src.llm.rag.pipline import run_ingest, run_rag

def run_rag_pipeline():
    run_ingest()
    run_rag()
