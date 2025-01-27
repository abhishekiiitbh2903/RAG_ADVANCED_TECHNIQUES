import json
import os

class AdvancedPdfLoader:
    def __init__(self, file_path):
        """
        Initialize the AdvancedPdfLoader class

        Parameters
        ----------
        file_path : str
            The path to the json file that contains the data extracted from a PDF

        Raises
        ------
        AssertionError
            If the file path is None, does not end with ".json", or does not exist
        """
        assert file_path is not None, "File path cannot be None"
        self.file_path = file_path
        assert self.file_path.endswith(".json"), "File must be a json file"
        assert os.path.exists(self.file_path), "File does not exist"
        self.data=self.load()

    def load(self):
        """
        Load the data from the json file

        Returns
        -------
        data : list
            A list of dictionaries, where each dictionary contains the data extracted from a PDF page
        """
        with open(self.file_path, 'r') as file:
            data = json.load(file)
        return data
    
    def table_extractor(self):
        """
        Extracts the tables from the PDF pages

        Returns
        -------
        tables : list
            A list of strings, where each string is a table extracted from the PDF pages
        """
        tables=[]
        for entry in self.data:
           if 'text_as_html' in entry['metadata']:
               tables.append(entry['metadata']['text_as_html'])
        return tables
    
    def text_extractor(self):
        """
        Extracts the text from the PDF pages

        Returns
        -------
        texts : list
            A list of strings, where each string is a text extracted from the PDF pages
        """
        texts=[]
        for entry in self.data:
           texts.append(entry['text'])
        return texts
     
    def __str__(self):
        """
        Returns a string representation of the AdvancedPdfLoader object

        Returns
        -------
        str
            A string representation of the AdvancedPdfLoader object
        """
        return f"AdvancedPdfLoader(file_path={self.file_path})"
    
    def combined_extractor(self):
        """
        Extracts both tables and text from the PDF pages

        Returns
        -------
        tuple
            A tuple of two lists, where the first list contains the extracted tables and the second list contains the extracted texts
        """
        return self.table_extractor(), self.text_extractor()
    




