import uuid
import logging
import chromadb
import getpass
import os
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from PyPDF2 import PdfReader
from langchain_openai import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv


logger = logging.getLogger(__name__)

load_dotenv()

if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = getpass.getpass(
        "Enter API key for OpenAI: ")

chat_model = ChatOpenAI(
    model="gpt-4o-mini", api_key=os.environ["OPENAI_API_KEY"])

app = FastAPI()

pdf_path = "Harry Potter AI.pdf"
client = chromadb.PersistentClient("./mycollection")
collection = None


class QuestionRequest(BaseModel):
    """Data model for a question request."""
    question: str


def read_pdf(file):
    """Read a PDF file and return its reader object."""
    result = PdfReader(file)
    return result


def extract_text_from_pdf(reader):
    """Extract and return text from each page of the PDF reader."""
    try:
        text = ""
        for page_num, page in enumerate(reader.pages):
            extract_text = page.extract_text()
            if extract_text:
                text += extract_text + "\n\n"
            else:
                logger.warning(f"Text not found {page_num}")

        return text
    except Exception as ex:
        logger.error(f"Error in extract text form pdf: {ex}")


def split_text_from_pdf(text, chunk_size=1000, chunk_overlap=200):
    """Split text into chunks with given size and overlap."""
    try:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=[". ", "... ", ", ", "! ", "? ", "\n\n", "\n", " ", ""],
        )

        return text_splitter.split_text(text)
    except Exception as ex:
        logger.error(f"Error in splitter a document: {ex}")


def create_collection(collection_name, client):
    """Create or retrieve a collection in the database."""
    try:
        collection = client.get_or_create_collection(
            name=collection_name, metadata={"hnsw:space": "cosine"})
        return collection
    except Exception as ex:
        logger.error(f"Error in creating a collection: {ex}")


def add_to_collection(text_chunks, collection):
    """Add text chunks to the collection with unique ids."""
    try:
        documents = []
        ids = []

        for idx, text in enumerate(text_chunks):
            random_id = str(uuid.uuid4())
            ids.append(f"chunk_id{idx}_unique_id_{random_id}")
            documents.append(text)

        collection.add(
            documents=documents,
            ids=ids
        )
        print(f"Added {len(documents)} chunks to the collection.")
    except Exception as ex:
        logger.error(f"Error to add in collection: {ex}")


@app.on_event("startup")
def startup_event():
    """Startup event to populate the database with PDF chunks."""
    global collection

    collection = create_collection("pdf_collection", client)

    logger.debug("Reading PDF...")
    reader = read_pdf(pdf_path)
    if not reader:
        return

    logger.debug("Extracting text from PDF...")
    pdf_text = extract_text_from_pdf(reader)

    logger.debug("Spliting text in chunks...")
    text_chunks = split_text_from_pdf(pdf_text)

    logger.debug("Adding chunks to the database...")
    add_to_collection(text_chunks, collection)

    logger.info("Database populated with successfully!")


@app.on_event("shutdown")
def shutdown_event():
    """Shutdown event to clean up the database."""
    global collection
    try:
        if collection:
            client.delete_collection("pdf_collection")
            logger.debug("Database clean up!")
    except Exception as ex:
        logger.error(f"Error in clean up the database: {ex}")


@app.post("/ask_ai")
async def ask_to_ai(request: QuestionRequest):
    """Process a question and return an AI-generated answer."""
    try:
        question = request.question

        results = collection.query(
            query_texts=[question],
            n_results=3
        )
        print(results)

        relevant_texts = [
            result[0] for result in results['documents']]

        context = " ".join(relevant_texts)

        response = chat_model(context + question)

        return {"answer": response.content}

    except Exception as ex:
        logger.error(f"Error while asking question: {ex}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
