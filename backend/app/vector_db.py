import os
import logging
import numpy as np
from app.config import settings

logger = logging.getLogger(__name__)

# Try to import chromadb and sentence_transformers
CHROMA_AVAILABLE = False
SENTENCE_TRANSFORMERS_AVAILABLE = False

try:
    import chromadb
    CHROMA_AVAILABLE = True
except ImportError:
    logger.warning("chromadb package not available. Vector database will run in mock/in-memory mode.")

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    logger.warning("sentence-transformers package not available. Semantic parser will fall back to TF-IDF.")

# ─── Embedding Client Setup ───────────────────────────────────────────────────
class EmbeddingClient:
    def __init__(self):
        self.model = None
        if SENTENCE_TRANSFORMERS_AVAILABLE:
            try:
                logger.info(f"Loading embedding model: {settings.EMBEDDING_MODEL_NAME}")
                self.model = SentenceTransformer(settings.EMBEDDING_MODEL_NAME)
                logger.info("Embedding model loaded successfully")
            except Exception as e:
                logger.error(f"Error loading SentenceTransformer ({e}). Using mock embedder.")
                self.model = None

    def get_embedding(self, text: str) -> list:
        if self.model:
            try:
                emb = self.model.encode(text)
                return emb.tolist()
            except Exception as e:
                logger.error(f"Embedding error: {e}")
        
        # Fallback pseudo-embedding (384 float vector from hash of string)
        np.random.seed(abs(hash(text)) % (2**32 - 1))
        return np.random.randn(384).tolist()

embedder = EmbeddingClient()

# ─── ChromaDB / Mock DB Setup ─────────────────────────────────────────────────
class VectorDB:
    def __init__(self):
        self.client = None
        self.collection = None
        self.mock_store = {} # Fallback in-memory dict: candidate_id -> (embedding, text, metadata)
        
        if CHROMA_AVAILABLE:
            try:
                os.makedirs(settings.CHROMA_DB_PATH, exist_ok=True)
                self.client = chromadb.PersistentClient(path=settings.CHROMA_DB_PATH)
                self.collection = self.client.get_or_create_collection(name="talentmind_candidates")
                logger.info("ChromaDB initialized successfully")
            except Exception as e:
                logger.error(f"ChromaDB initialization failed ({e}). Using in-memory fallback.")
                self.client = None
                self.collection = None

    def add_candidate(self, candidate_id: str, profile_text: str, metadata: dict = None):
        self.add_candidates_batch([candidate_id], [profile_text], [metadata or {}])

    def add_candidates_batch(self, candidate_ids: list, profile_texts: list, metadatas: list = None):
        if not candidate_ids:
            return
        if metadatas is None:
            metadatas = [{} for _ in candidate_ids]
            
        embeddings = []
        if embedder.model:
            try:
                embeddings = embedder.model.encode(profile_texts).tolist()
            except Exception as e:
                logger.error(f"Batch embedding error: {e}")
                embeddings = [embedder.get_embedding(t) for t in profile_texts]
        else:
            embeddings = [embedder.get_embedding(t) for t in profile_texts]

        if self.collection:
            try:
                self.collection.upsert(
                    ids=candidate_ids,
                    embeddings=embeddings,
                    documents=profile_texts,
                    metadatas=metadatas
                )
                return
            except Exception as e:
                logger.error(f"ChromaDB batch upsert error: {e}")

        # Fallback mock store
        for cid, emb, p_text, meta in zip(candidate_ids, embeddings, profile_texts, metadatas):
            self.mock_store[cid] = (emb, p_text, meta)

    def search_candidates(self, query_text: str, top_n: int = 50) -> dict:
        query_emb = embedder.get_embedding(query_text)
        
        if self.collection:
            try:
                results = self.collection.query(
                    query_embeddings=[query_emb],
                    n_results=min(top_n, max(len(self.mock_store), 100))
                )
                
                # Format response: candidate_id -> similarity_score
                scores = {}
                if results and 'ids' in results and len(results['ids']) > 0:
                    ids = results['ids'][0]
                    # Chroma returns distance (e.g. L2 distance or cosine distance).
                    # We normalize it to a similarity score between 0 and 1.
                    distances = results['distances'][0] if 'distances' in results else [0.5] * len(ids)
                    for cid, dist in zip(ids, distances):
                        # Convert distance to similarity
                        similarity = max(0.0, min(1.0, 1.0 - (dist / 2.0)))
                        scores[cid] = similarity
                return scores
            except Exception as e:
                logger.error(f"ChromaDB query error ({e}). Using mock search.")
        
        # Mock Search (Cosine similarity using numpy)
        scores = {}
        q_vec = np.array(query_emb)
        q_norm = np.linalg.norm(q_vec) or 1.0
        
        for cid, (c_emb, _, _) in self.mock_store.items():
            c_vec = np.array(c_emb)
            c_norm = np.linalg.norm(c_vec) or 1.0
            similarity = float(np.dot(q_vec, c_vec) / (q_norm * c_norm))
            # Normalize to 0-1 range
            scores[cid] = max(0.0, min(1.0, (similarity + 1.0) / 2.0))
            
        # Sort scores and return
        sorted_scores = dict(sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_n])
        return sorted_scores

vector_db = VectorDB()
