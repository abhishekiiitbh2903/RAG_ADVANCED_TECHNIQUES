# Retrieval-Augmented Generation (RAG) System

## Overview
This project implements an end-to-end **Retrieval-Augmented Generation (RAG)** system, designed to intelligently handle queries by combining retrieval and generative techniques. The system supports both **offline** and **online** modes, catering to diverse user requirements while maintaining data security and scalability.

## Key Features
- **Offline Mode (Confidential Requests):**
  - Utilizes the **Ollama** model running locally on the user's system.
  - Ensures sensitive or confidential documents are processed securely without leaving the local environment.

- **Online Mode (Non-Confidential Requests):**
  - Leverages the **LLaMA model** hosted on **Groq** infrastructure for scalable and efficient processing.

- **Dynamic Request Handling:**
  - Automatically routes requests based on confidentiality requirements.

- **Efficient Retrieval Pipeline:**
  - Retrieves relevant context from indexed documents for accurate query resolution.
 
## App Flow
1. **Streamlit UI Interaction:**
   - The user visits the Streamlit UI and selects whether they have any questions related to the **BLUEBOOK**.
     - If the user selects **Yes**:
       - The sidebar for file upload and vector store generation is hidden.
       - The pre-prepared vector store for the BLUEBOOK is used, created using advanced techniques.
     - If the user selects **No**:
       - The user is prompted to upload a file.

2. **Document Confidentiality:**
   - After uploading the file, the user is asked whether the document is confidential:
     - **Confidential Documents:**
       - The request is processed using Ollama running on the local computer.
       - For knowledge base preparation, **Ollama Nomic Embeddings** and the **Chat Model** are used.
     - **Non-Confidential Documents:**
       - **Sentence Transformer Embeddings** are used for embedding generation.
       - The **LLaMA model** is used for language generation.

3. **Vector Store Preparation:**
   - While the vector store is being prepared, the user cannot ask any questions until the process is complete.

## Unique Features

### Knowledge Base Preparation
Once a PDF is uploaded for knowledge base preparation, the following steps are followed:
1. **Chunking and Summarization**:
   - The document is divided into smaller chunks.
   - A summary is generated for each chunk.
2. **Linking Summaries and Chunks**:
   - Each summary and its corresponding chunk are assigned a unique ID.
3. **Embedding and Storage**:
   - The summary is embedded and stored in a vector database (vectordb).
   - The chunk is stored in MongoDB.

### Retrieval Process
1. **User Query**:
   - The user submits a question.
2. **Chunk Retrieval**:
   - Five relevant chunks (summaries of chunks) are identified based on semantic similarity to the query.
3. **Related Chunk Retrieval**:
   - Related chunks corresponding to the selected summaries are retrieved from MongoDB.
4. **Ranking**:
   - A ranker function evaluates the chunks and selects the top three.
5. **Response Generation**:
   - The question and the top three chunks are passed to the LLM to generate a response.

## Technical Implementation
This branch integrates both local and cloud-based RAG pipelines:
- **Local Mode**: Ensures confidentiality by processing sensitive documents locally using Ollama.
- **Cloud Mode**: Optimizes processing for non-confidential documents using Groq's Llama services.

---
# Steps to reproduce the code:
#### Create a Virtual Environment 

## Step 1: Install Python 3.11
Make sure Python 3.11 is installed on your system. You can download it from the [official Python website](https://www.python.org/downloads/).

### Verify Installation
Open a command prompt and check the Python version:
```bash
python --version
```
Ensure it shows Python 3.11.x.

## Step 2: Open Command Prompt
Open the Command Prompt (CMD) or PowerShell on your Windows machine.

## Step 3: Navigate to Your Project Directory
Use the `cd` command to navigate to the directory where you want to create the virtual environment:
```bash
cd path\to\your\project
```

## Step 4: Create the Virtual Environment
Run the following command to create a virtual environment:
```bash
python -m venv env_name
```
Replace `env_name` with the name you want for your virtual environment (e.g., `venv`).

## Step 5: Activate the Virtual Environment
Activate the virtual environment using the following command:
```bash
env_name\Scripts\activate
```
After activation, you should see `(env_name)` at the beginning of the command prompt.

## Step 6: Verify Virtual Environment
Check the Python version to ensure the virtual environment is using Python 3.11:
```bash
python --version
```
## Step 7: Install the following libraries:
```bash
pip install langchain==0.0.354 langchain-community==0.0.8 langchain-groq==0.2.3 sentence-transformers==3.3.1 pymongo==4.10.1 ollama==0.4.6 streamlit==1.41.1 pypdf==5.2.0 python-dotenv==1.0.1 chromadb==0.6.3
```

#### Download Ollama

1. Visit the [Ollama installation page](https://ollama.com/download) and download the appropriate version for your operating system.
2. Install Ollama by following the provided instructions for your platform.
3. Verify the installation by running the following command:
   ```bash
   ollama --version
   ```

### Step 2: Pull Nomic Embeddings and Llama Model
1. Ensure Ollama is installed and running on your system.
2. Open a terminal and use the following command to pull the Nomic embeddings model:
   ```bash
   ollama pull <nomic-embeddings-model-name>
   ```
   Replace `<nomic-embeddings-model-name>` with the exact model name specified in  `config.yml` file.

3. Similarly, pull the Llama model:
   ```bash
   ollama pull <llama-model-name>
   ```
   Replace `<llama-model-name>` with the model name from  `config.yml` file.

### Step 3: Validate Models and Configuration
1. Open the `config.yml` file located in the project directory.
2. Check that the model names for embeddings and LLM match the ones pulled earlier:
   ```yaml
   embeddings_model: <nomic-embeddings-model-name>
   llm_model: <llama-model-name>
   ```
   Replace `<nomic-embeddings-model-name>` and `<llama-model-name>` with the actual model names.

3. Test the models by running the following command:
   ```bash
   ollama list
   ```
   Ensure both models appear in the list of available models.

### Step 4: Start Ollama Server
1. Launch the Ollama server by running:
   ```bash
   ollama serve
   ```
2. Confirm the server is running and accessible.

### Setting up Environment Variables (.env)
```bash
GROQ_API_KEY= ****************************************
MONGO_URI= *******************************************
```
Now your project setup is completed 😊. To launch streamlit ui
```bash
streamlit run main.py
```
# Project Author and Support 💁‍♂️
This project was developed by **Abhishek Singh** under the guidance and leadership of **Aman Srivastava**. If you encounter any issues or have queries, feel free to reach out via email at [abhishekrathore1806@gmail.com](mailto:abhishekrathore1806@gmail.com).



## Current Version: 0.1

This version includes basic functionality for data chunking and retrieval, with room for improvement in efficiency.

---

## TODO:

### 1. **Improve Chunking Strategy**
   - Assess and optimize the current chunking approach to handle larger datasets more efficiently.
   - Test different chunk sizes and segmentation algorithms to find the optimal balance between memory usage and processing speed.
   - Incorporate a dynamic chunking mechanism that adapts to data size and content.

### 2. **Enhance Retrieval Process**
   - Research and integrate efficient algorithms for retrieval tailored to our use case, such as vector-based search or more advanced indexing methods.
   - Implement multi-threading or parallel processing to speed up retrieval times, especially for large datasets.
   - Test retrieval performance under various data loads to identify potential bottlenecks and optimize accordingly.

---

## Version 0.2 Plan:

- Release a new version that focuses on improving:
   1. Chunking strategy for better memory and processing efficiency.
   2. Retrieval process incorporating tailored, efficient algorithms.
   3. Optimization of the overall system to handle larger datasets and provide faster retrieval times.
  
---

## Conclusion

As we continue to improve and refine our approach, we are committed to delivering an optimized and efficient solution for data chunking and retrieval. With version 0.2, we aim to make significant strides towards achieving faster processing times, enhanced performance, and scalability. Your contributions, feedback, and collaboration are key to our success, and we look forward to building something truly impactful together.

Stay tuned for future updates, and feel free to get involved!

Happy coding! 🚀












