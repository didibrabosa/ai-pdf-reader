# RAG PDF Reader

## Project Description
The **RAG PDF Reader** is an application that implements a Retrieval-Augmented Generation (**RAG**) system using **FastAPI**. The app reads a specific PDF file ("Harry Potter AI.pdf"), extracts its text, splits it into **chunks**, and stores these chunks in a vector database with **ChromaDB**. When you ask a question, the system retrieves the most relevant text chunks and uses an **OpenAI** model to generate an answer.

### How It Works
1. Startup Process:
   - The PDF file is read and its text is extracted.
   - The extracted text is split into chunks.
   - The chunks are stored in a ChromaDB collection.
   - The response is returned to the user via a **FastAPI**.
2. Query Processing:
   - A POST request is sent to the /ask_ai endpoint with a question.
   - The system retrieves the top 3 relevant chunks from the collection.
   - The retrieved chunks are combined to form a context.
   - The context and question are sent to an OpenAI model (gpt-4o-mini) to generate an answer.
3. Shutdown Process:
   - The ChromaDB collection is deleted to clean up the database.

## Requirements
To run this project, install the following dependencies:

```bash
pip install -r requirements.txt
```

The `requirements.txt` file includes:
- **FastAPI**: Framework for building the API.
- **uvicorn**: ASGI server for FastAPI.
- **python-dotenv**: For managing environment variables.
- **langchain**: Library for interacting with LLMs.
- **langchain and langchain-openai**: For interacting with OpenAI models.
- **chromadb**: Vector database for semantic searches.
- **PyPDF2**: Library for reading PDFs.
- **pydantic**: For data validation.

## How to Use
1.Set Up Your API Key:
    Create a .env file or set the environment variable OPENAI_API_KEY with your OpenAI API key.
    If not set, the application will prompt you to enter the key at startup.
2. Select a PDF:
   Choose a PDF of your choice and reference the path or use the example bellow.
3. Start the application by running:
   ```bash
   uvicorn main:app --reload
   ```
4. Ask a Question:
   Send a POST request to the /ask_ai endpoint with a JSON payload like:
   ```
   json
   {
     "question": "Your question about the PDF content"
   }
   ```
   The application will return an answer based on the extracted content from the PDF.
