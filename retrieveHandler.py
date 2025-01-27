from mongoHandler import mongoCollector
from rankingHandler import RerankedDocument
import itertools
from embeddingHandler import embeddingHandler
from configManager import configManager

config = configManager()

class Retriever:
    def __init__(self, query, is_confidential=False):
        self.query = query
        self.is_confidential = is_confidential
        if self.is_confidential:
            self.persist_directory = config.persist_directory_online
            self.is_ollama_embedding = True
        else:
            self.persist_directory = config.persist_directory_hf
            self.is_ollama_embedding = False
        self.embedding_master = embeddingHandler(self.persist_directory, is_ollama_embedding=self.is_ollama_embedding)
        if self.is_ollama_embedding:
            self.embedding_model = self.embedding_master.prepare_ollama_vectorDB()
        else:
            self.embedding_model = self.embedding_master.prepare_hf_vectorDB()
        self.vectordb = self.embedding_model

        self.results = self.get_relevant_documents()

        self.document_ids = list(itertools.chain.from_iterable(self.results.get("ids", [])))
        self.texts = mongoCollector().get_data(self.document_ids)
        self.ranked_docs, self.ranked_ids = RerankedDocument(self.texts, self.query).rank_documents()

    def get_relevant_documents(self):
        return self.vectordb.query(query_texts=[self.query], n_results=5)


if __name__ == "__main__":
    uploaded_query = "Tell me about the dataset used?"
    processed_query = "Tell me about Self Attention?"
    retriever = Retriever(uploaded_query)
    ranked_docs, ranked_ids = retriever.ranked_docs, retriever.ranked_ids
    print(ranked_docs)
