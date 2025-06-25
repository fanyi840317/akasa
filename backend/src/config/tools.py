from enum import Enum
from typing import Dict, Any


class RAGProvider(str, Enum):
    LLAMA_INDEX = "llama_index"
    LANGCHAIN = "langchain"


SELECTED_RAG_PROVIDER = RAGProvider.LLAMA_INDEX


def load_tools_config() -> Dict[str, Any]:
    # This is a placeholder implementation. In a real application, this would
    # load the configuration from a file (e.g., YAML or JSON).
    return {
        "crawl_mystery_events": {
            "description": "Crawl mysterious events from various sources.",
            "parameters": {
                "source": {"type": "string", "description": "The source to crawl from."}
            },
        },
        "search_academic_papers": {
            "description": "Search for academic papers on a given topic.",
            "parameters": {
                "query": {"type": "string", "description": "The search query."}
            },
        },
    }