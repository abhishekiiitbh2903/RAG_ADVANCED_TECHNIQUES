import yaml,os
from dotenv import load_dotenv
load_dotenv()


class configManager:
    def __init__(self):
        base_dir=os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(base_dir,"config.yml")
        with open(config_path, "r") as cfg:
            app_config = yaml.load(cfg, Loader=yaml.FullLoader)

        
        self.model_name=app_config["llm_config"]["model_name"]
        self.summary_system_prompt=app_config["llm_config"]["summary_system_prompt"]
        self.answer_system_prompt=app_config["llm_config"]["answer_system_prompt"]
        self.answer_system_prompt_ollama=app_config["llm_config"]["answer_system_prompt_ollama"]
        self.GROQ_API_KEY=os.getenv("GROQ_API_KEY")
        self.MONGO_URI=os.getenv("MONGO_URI")
        self.ollama_embedding_url=app_config["ollama_config"]["ollama_embedding_url"]
        self.ollama_model_name=app_config["ollama_config"]["ollama_model_name"]
        self.ollama_chat_model=app_config["ollama_config"]["ollama_chat_model"]

        self.persist_directory=app_config["directory_config"]["persist_directory"]
        self.persist_directory_online=app_config["directory_config_online"]["persist_directory"]
        self.persist_directory_hf=app_config["directory_config_online"]["persist_directory_hf"]
        self.hf_model_name=app_config["HuggingFace"]["model_name"]








