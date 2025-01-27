from retrieveHandler import Retriever
from llmHandler import llmHandler
import streamlit as st

class AnswerGenerator:
    def __init__(self, question, is_confidential=False):        
        self.question = question
        self.is_confidential = is_confidential
        self.retriever = Retriever(self.question, is_confidential=self.is_confidential)
        self.ranked_docs = self.retriever.ranked_docs
        self.answer_chain = None if self.is_confidential else llmHandler(is_answer=True).generate_chain()

    def generate_answer(self):
        if not self.ranked_docs:
            return "No relevant documents found."
        result = self.answer_chain.invoke({"context": self.ranked_docs, "question": self.question})
        return result

    def generate_ollama_answer(self):
        if not self.ranked_docs:
            return "No relevant documents found."
        response = llmHandler(is_answer=True).generate_response_ollama(self.ranked_docs, self.question)
        st.write("Generating response from Ollama...")
        final_answer = ""
        for chunk in response:
            if chunk["done"] is False:
                final_answer += chunk["message"]["content"]
            else:
                break
        return final_answer

    def get_answer(self):
        if self.is_confidential:
            return self.generate_ollama_answer()
        else:
            return self.generate_answer()


if __name__ == "__main__":
    question = input("Enter your question: ")
    is_confidential = input("Is this confidential? (yes/no): ").strip().lower() == "yes"
    answer_generator = AnswerGenerator(question, is_confidential=is_confidential)
    answer = answer_generator.get_answer()

    if isinstance(answer, str):
        print(answer)
    else:  
        for chunk in answer: 
            print(chunk, end="")
 