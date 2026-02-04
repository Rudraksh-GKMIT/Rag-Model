import logging
from pathlib import Path
from src.llm.config import RAGConfig


def setup_logging():
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    log_file = log_dir / "rag_model.log"

    logging.basicConfig(
        level=RAGConfig.LOG_LEVEL,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            # logging.StreamHandler(),
        ],
    )
