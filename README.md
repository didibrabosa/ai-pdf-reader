# RAG PDF Reader

## Project Description
The **RAG PDF Reader** is an application that implements a **Retrieval-Augmented Generation (RAG)** system, allowing users to upload PDF files and ask questions about their content. The responses are generated based on the extracted information from the document using **OpenAI models** to process the queries.

### How It Works
1. The uploaded PDF is processed and split into text chunks.
2. The chunks are stored in a **vector database** using **ChromaDB**.
3. When a user asks a question, the application retrieves the most relevant text chunks and passes them to an **OpenAI language model**, which generates a response.
4. The response is returned to the user via a **Flask REST API**.

## Requirements
To run this project, install the following dependencies:

```bash
pip install -r requirements.txt
```

The `requirements.txt` file includes:
- **Flask**: Framework for building the REST API.
- **python-dotenv**: Environment variable management.
- **langchain**: Library for interacting with LLMs.
- **langchain-openai**: LangChain connector for OpenAI models.
- **langchain-community**: Additional components for LangChain.
- **chromadb**: Vector database for semantic searches.
- **PyPDF2**: Library for reading PDFs.
- **sentence-transformers**: Embedding model to convert text into vectors.

## How to Use
1. Start the application by running:
   ```bash
   python main.py
   ```
2. Upload a PDF file and send a question to the `/read_pdf` endpoint via a **POST request**.
3. The application will process the document and return a response based on the extracted information.

This project can be expanded to support multiple documents, different file formats, and integrations with other AI models for even more precise responses.

