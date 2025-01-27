import chromadb
from chromadb.utils.embedding_functions.ollama_embedding_function import OllamaEmbeddingFunction
from configManager import configManager
from sentence_transformers import SentenceTransformer
from log import get_logger

class HFEmbeddingFunction:
    def __init__(self, model_name):
        self.model = SentenceTransformer(model_name)

    def __call__(self, input):
        if isinstance(input, str):
            input = [input]
        return self.model.encode(input).tolist()

class embeddingHandler:
    def __init__(self, persist_directory,is_ollama_embedding=False):
        self.config = configManager()
        self.persist_directory = persist_directory
        self.logger = get_logger()

        self.logger.info(f"Initializing embeddingHandler with persist_directory: {persist_directory}")
        if is_ollama_embedding:
            self.ollama_embedding = OllamaEmbeddingFunction(
                url=self.config.ollama_embedding_url,
                model_name=self.config.ollama_model_name,
            )
            self.logger.info("OllamaEmbeddingFunction initialized")
        else:
            self.hf_embedding_model = HFEmbeddingFunction(self.config.hf_model_name)
            self.logger.info("HFEmbeddingFunction initialized")

    def prepare_ollama_vectorDB(self):
        self.logger.info("Preparing Ollama VectorDB...")
        chroma_client = chromadb.PersistentClient(path=self.persist_directory)
        vectordb = chroma_client.get_or_create_collection(
            name="my_collection",
            embedding_function=self.ollama_embedding,
            metadata={"hnsw:space": "cosine"},
        )
        self.logger.info("Ollama VectorDB created or retrieved")
        return vectordb

    def prepare_hf_vectorDB(self):
        self.logger.info("Preparing HF VectorDB...")
        chroma_client = chromadb.PersistentClient(path=self.persist_directory)
        vectordb = chroma_client.get_or_create_collection(
            name="my_collection",
            embedding_function=self.hf_embedding_model,
            metadata={"hnsw:space": "cosine"},
        )
        self.logger.info("HF VectorDB created or retrieved")
        return vectordb