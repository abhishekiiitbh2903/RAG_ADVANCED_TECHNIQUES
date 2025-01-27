from llmHandler import llmHandler
from tqdm import tqdm
from dataLoader import AdvancedPdfLoader


class SummaryGenerator():
    def __init__(self,file_path=None,texts=[]):
        self.file_path=file_path
        self.texts=texts
        self.summarize_chain = llmHandler(is_answer=False).generate_chain()
    def generate_summaries(self):
        loader = AdvancedPdfLoader(self.file_path)
        tables, texts = loader.combined_extractor()
        with tqdm(total=len(tables)) as pbar:
            summaries_table= []
            for table in tables:
                summary = self.summarize_chain.invoke({"element": table})
                summaries_table.append(summary)
                pbar.update(1)

        with tqdm(total=len(texts)) as pbar:
            summaries_text= []
            for text in texts:
                summary = self.summarize_chain.invoke({"element": text})
                summaries_text.append(summary)
                pbar.update(1)

        return tables,texts,summaries_table,summaries_text
    
    def generate_summaries_text(self):
        with tqdm(total=len(self.texts)) as pbar:
            summaries_text= []
            for text in self.texts:
                summary = self.summarize_chain.invoke({"element": text})
                summaries_text.append(summary)
                pbar.update(1)

        return summaries_text
    
        



    




