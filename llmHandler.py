from configManager import configManager
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import ollama

config=configManager()
model_name=config.model_name
summary_system_prompt=config.summary_system_prompt
answer_system_prompt=config.answer_system_prompt
answer_system_prompt_ollama=config.answer_system_prompt_ollama
GROQ_API_KEY=config.GROQ_API_KEY

class llmHandler:
    def __init__(self,is_answer=False):
        self.prompt_text=summary_system_prompt if is_answer==False else answer_system_prompt
        self.ollama_prompt_text=answer_system_prompt_ollama
    
        
    def generate_chain(self):
        prompt = ChatPromptTemplate.from_template(self.prompt_text)

        self.model = ChatGroq(temperature=0.5, model="llama-3.1-8b-instant",api_key=GROQ_API_KEY)
        self.chain = prompt | self.model | StrOutputParser()

        return self.chain
    def generate_response_ollama(self,context,prompt):
        response = ollama.chat(
        model=config.ollama_chat_model,
        stream=True,
        messages=[
            {
                "role": "system",
                "content": answer_system_prompt_ollama,
            },
            {
                "role": "user",
                "content": f"Context: {context}, Question: {prompt}",
            },
             ],
            )
        return response
    
    
