from sentence_transformers import CrossEncoder

class RerankedDocument:
    def __init__(self, documents, question):
        self.documents = documents
        self.question = question

    def rank_documents(self):
        relevant_text = ""
        relevant_text_ids = []

        encoder_model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
        ranks = encoder_model.rank(self.question, self.documents, top_k=3)
        for rank in ranks:
            relevant_text += self.documents[rank["corpus_id"]]
            relevant_text_ids.append(rank["corpus_id"])

        return relevant_text, relevant_text_ids
    


