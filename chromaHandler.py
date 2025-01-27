import chromadb
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

class Embedder:
    def __init__(self):
        config=configManager()
        logger=get_logger()
        self.persist_directory=config.persist_directory_hf
        self.hf_embedding_model = HFEmbeddingFunction(config.hf_model_name)
        self.vectordb=self.prepare_vectorDB()


    def prepare_vectorDB(self):
        chroma_client=chromadb.PersistentClient(path=self.persist_directory)
        self.vectordb = chroma_client.get_or_create_collection(
            name="my_collection",
            embedding_function=self.hf_embedding_model,
            metadata={"hnsw:space": "cosine"},   
        )
        return self.vectordb
    
    def insert_data(self,data):
        assert len(data) > 0, "Data cannot be empty"
        documents,metadatas,ids=[],[],[]
        for doc in data:
            documents.append(doc.page_content)
            metadatas.append(doc.metadata)
            ids.append(doc.metadata['id_key'])
        
        self.vectordb.upsert(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
            



    
    


