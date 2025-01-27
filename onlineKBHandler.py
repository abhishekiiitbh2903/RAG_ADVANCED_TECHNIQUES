import os
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from configManager import configManager
from typing import List
from embeddingHandler import embeddingHandler
from summaryHandler import SummaryGenerator
from langchain.schema.document import Document
from mongoHandler import mongoCollector
import uuid

config = configManager()

class PrepareVectorDBOnline:
    def __init__(self, file_path, chunk_size=2000, chunk_overlap=200,is_confidential=False, is_ollama_embedding=False):
        self.file_path = file_path
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.is_confidential = is_confidential
        self.is_ollama_embedding = is_ollama_embedding

        if self.is_confidential:
            self.persist_directory = config.persist_directory_online
            self.is_ollama_embedding = True
        else:
            self.persist_directory = config.persist_directory_hf

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )

        self.embedding_handler = embeddingHandler(self.persist_directory, is_ollama_embedding=self.is_ollama_embedding)
        if self.is_ollama_embedding:
            self.embedding_model = self.embedding_handler.prepare_ollama_vectorDB()
        else:
            self.embedding_model = self.embedding_handler.prepare_hf_vectorDB()

    def load_document(self):
        docs = []
        docs.extend(PyPDFLoader(self.file_path).load())
        print(f"Number of pages: {len(docs)}")
        return docs

    def __chunk_documents(self, docs: List) -> List:
        print("Chunking documents...")
        chunked_documents = self.text_splitter.split_documents(docs)
        print("Number of chunks:", len(chunked_documents), "\n\n")
        return chunked_documents
    
    def summary_generator(self):
        docs = self.load_document()
        chunked_documents = self.__chunk_documents(docs)
        documents=[doc.page_content for doc in chunked_documents]
        summary_documents=SummaryGenerator(file_path=None,texts=documents).generate_summaries_text()
        print(f"length of summary_documents: {len(summary_documents)}")
        return documents,summary_documents

    def prepare_and_save_vectordb(self):
        vectordb=self.embedding_model
        unique_ids,summary_docs,original_chunks=self.create_document()
        documents,metadatas,ids=[],[],[]
        for doc in summary_docs:
            documents.append(doc.page_content)
            metadatas.append(doc.metadata)
            ids.append(doc.metadata['id_key'])

        print(f"First summary_doc: {summary_docs[0].page_content}")    

        vectordb.upsert(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        print("VectorDB is created and saved.")
        print("Number of vectors in vectordb:", vectordb.count(), "\n\n")
        print("Inserting into MongoDB ...")
        mongo_collector = mongoCollector()
        mongo_collector.insert_data(unique_ids,original_chunks)
        return vectordb
    
    def create_document(self):
        documents,summary_documents=self.summary_generator()
        doc_ids_texts = [str(uuid.uuid4()) for _ in documents]
        summary_texts_documents = [
            Document(page_content=summary, metadata={"id_key": doc_ids_texts[i]}) for i, summary in enumerate(summary_documents)
        ]
        return doc_ids_texts,summary_texts_documents,documents



if __name__ == "__main__":
    file_path = os.path.join(os.getcwd(), "..", "data", "docs", "Electricity_Thefting.pdf")
    print(file_path)
    
    loader = PrepareVectorDBOnline(file_path,is_confidential=False)
    
    vectordb = loader.prepare_and_save_vectordb()
    print("Vector DB Created Successfully, Finding you length of vectordb")
    print(f"Number of vectors in vectordb: {vectordb.count()}")