import os
import sys
import uuid
import chromadb
from dotenv import load_dotenv

# Ensure we can import config from the root directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import CHROMA_COLLECTION

# Ensure environment variables are loaded
load_dotenv()

class OracleVectorStore:
    def __init__(self, persist_directory: str = "chroma_db"):
        """Initialize ChromaDB wrapper."""
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(name=CHROMA_COLLECTION)

    def add_decision_case(self, decision: str, outcome: str, domain: str, metadata: dict) -> str:
        """
        Stores historical decision cases.
        """
        case_id = str(uuid.uuid4())
        
        # Combine decision and outcome for the embedding document
        document = f"Decision: {decision}\nOutcome: {outcome}\nDomain: {domain}"
        
        # Merge into metadata
        enriched_metadata = metadata.copy() if metadata else {}
        enriched_metadata["domain"] = domain
        enriched_metadata["outcome"] = outcome
        
        # ChromaDB metadata values must be strings, ints, floats or bools. 
        # Convert any complex types or none to string to avoid errors.
        for key, value in enriched_metadata.items():
            if not isinstance(value, (str, int, float, bool)):
                enriched_metadata[key] = str(value)
        
        self.collection.add(
            documents=[document],
            metadatas=[enriched_metadata],
            ids=[case_id]
        )
        return case_id

    def find_similar_decisions(self, query: str, n_results: int = 5) -> list:
        """
        Finds historically similar decisions.
        """
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            similar_decisions = []
            if results and results.get("documents") and len(results["documents"]) > 0:
                docs = results["documents"][0]
                metas = results["metadatas"][0]
                distances = results.get("distances", [[0]*len(docs)])[0]
                
                for doc, meta, dist in zip(docs, metas, distances):
                    similar_decisions.append({
                        "document": doc,
                        "metadata": meta,
                        "distance": dist
                    })
            return similar_decisions
        except Exception as e:
            print(f"Error finding similar decisions: {e}")
            return []

    def clear(self):
        """
        Resets collection.
        """
        try:
            self.client.delete_collection(name=CHROMA_COLLECTION)
            self.collection = self.client.get_or_create_collection(name=CHROMA_COLLECTION)
        except Exception as e:
            print(f"Error clearing collection: {e}")
