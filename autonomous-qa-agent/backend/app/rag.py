import os
from typing import List, Dict
from pathlib import Path

try:
    from sentence_transformers import SentenceTransformer
    import chromadb
    DEPS_AVAILABLE = True
except ImportError:
    DEPS_AVAILABLE = False

from .html_parser import parse_html_structure
from .llm_integration import generate_test_cases_with_llm

# Initialize
if DEPS_AVAILABLE:
    try:
        MODEL = SentenceTransformer("all-MiniLM-L6-v2")
        CHROMA_DIR = os.path.join(os.getcwd(), "vector_store")
        os.makedirs(CHROMA_DIR, exist_ok=True)
        
        client = chromadb.PersistentClient(path=CHROMA_DIR)
        collection = client.get_or_create_collection("docs")
    except Exception as e:
        print(f"Error initializing RAG: {e}")
        DEPS_AVAILABLE = False

# Global HTML structure
HTML_STRUCTURE = {}

def set_html_structure(html_path: str):
    """Parse and store YOUR checkout.html structure"""
    global HTML_STRUCTURE
    HTML_STRUCTURE = parse_html_structure(html_path)
    print(f"✓ Parsed HTML - Found {len(HTML_STRUCTURE.get('features', []))} features")


def retrieve_context(prompt: str, n_results: int = 5) -> str:
    """Retrieve relevant context from vector store"""
    if not DEPS_AVAILABLE:
        return ""
    
    try:
        emb = MODEL.encode(prompt).tolist()
        res = collection.query(query_embeddings=[emb], n_results=n_results)

        docs = []
        if "documents" in res and len(res["documents"]) > 0:
            docs = res["documents"][0]

        return "\n\n".join(docs)
    except Exception as e:
        print(f"Error retrieving context: {e}")
        return ""


def generate_test_cases_from_prompt(prompt: str) -> List[Dict]:
    """
    Generate test cases using documentation context and HTML structure.
    This is GROUNDED in your actual documents and HTML.
    """
    context = retrieve_context(prompt)
    
    # Use LLM integration with YOUR HTML structure
    test_cases = generate_test_cases_with_llm(prompt, context, HTML_STRUCTURE)
    
    return test_cases