from langchain.schema.document import Document
import uuid
from summaryHandler import SummaryGenerator
from chromaHandler import Embedder
from mongoHandler import mongoCollector

class prepareKnowledgeBase:
    def __init__(self,file_path,is_new=False):
        if is_new:
            self.generator=SummaryGenerator(file_path,texts=[])
            self.tables, self.texts, self.summaries_table, self.summaries_text = self.generator.generate_summaries()
            print(f"length of tables: {len(self.tables)}")
            print(f"length of texts: {len(self.texts)}")
            print(f"length of summaries_table: {len(self.summaries_table)}")
            print(f"length of summaries_text: {len(self.summaries_text)}")
            self.summary_texts_documents, self.summary_tables_documents, self.doc_ids_texts, self.doc_ids_tables = self.create_document()
            print(f"length of summary_texts_documents: {len(self.summary_texts_documents)}")
            print(f"length of summary_tables_documents: {len(self.summary_tables_documents)}")
            print(f"length of doc_ids_texts: {len(self.doc_ids_texts)}")
            print(f"length of doc_ids_tables: {len(self.doc_ids_tables)}")
            if Embedder().vectordb.count() > 0:
                print("Vector DB already exists, skipping creation")
                return
            self.text_summary_embeddings = Embedder().insert_data(self.summary_texts_documents)
            self.table_summary_embeddings = Embedder().insert_data(self.summary_tables_documents)
            print("Vector DB Created Successfully, Finding you length of vectordb")
            print(f"Number of vectors in vectordb: {Embedder().vectordb.count()}")
            self.text_embeddings=mongoCollector().insert_data(self.doc_ids_texts,self.texts)
            self.table_embeddings=mongoCollector().insert_data(self.doc_ids_tables,self.tables)


    def create_document(self):
        doc_ids_texts = [str(uuid.uuid4()) for _ in self.texts]
        summary_texts_documents = [
            Document(page_content=summary, metadata={"id_key": doc_ids_texts[i]}) for i, summary in enumerate(self.summaries_text)
        ]

        doc_ids_tables = [str(uuid.uuid4()) for _ in self.tables]
        summary_tables_documents = [
            Document(page_content=summary, metadata={"id_key": doc_ids_tables[i]}) for i, summary in enumerate(self.summaries_table)
        ]
        return summary_texts_documents , summary_tables_documents , doc_ids_texts , doc_ids_tables
    



