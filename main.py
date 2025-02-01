import logging
import chromadb
import getpass
import uuid
import os
from langchain_openai import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from fastapi import FastAPI
from PyPDF2 import PdfReader
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

load_dotenv()

if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = getpass.getpass(
        "Enter API key for OpenAI: ")

app = FastAPI()

chat_model = ChatOpenAI(
    model="gpt-4o-mini", api_key=os.environ["OPENAI_API_KEY"])

client = chromadb.PersistentClient("./mycollection")

collection = None

pdf_path = "diego-barbosa-vasconcelos-dev.pdf"


def read_pdf(file):
    return PdfReader(file)


def extract_text_from_pdf(reader):
    try:
        text = ""
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text() or ""
        return text
    except Exception as ex:
        logger.error(f"Error in extract text form pdf: {ex}")


def create_collection(collection_name, client):
    try:
        collection = client.get_or_create_collection(
            name=collection_name, metadata={"hnsw:space": "cosine"})
        return collection
    except Exception as ex:
        logger.error(f"Error in creating a collection: {ex}")


def add_to_collection(text_chunks, collection):
    try:
        documents = []
        ids = []

        for idx, text in enumerate(text_chunks):
            random_id = str(uuid.uuid4())
            ids.append(f"chunk_id{idx}_unique_id_{random_id}")
            documents.append(text.pages_content)

        collection.add(
            documents=documents,
            ids=ids
        )
    except Exception as ex:
        logger.error(f"Error to add in collection: {ex}")


def text_splitter(
        separators: list = None, chunk_size: int = 1000,
        chunk_overlap: int = 200, content: str = None):
    try:
        text_splitter = RecursiveCharacterTextSplitter(
            separators=separators,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

        text_chunks = text_splitter.create_documents([content])
        return text_chunks
    except Exception as ex:
        logger.error(f"Error in splitter a document: {ex}")


@app.on_event("startup")
def statup_event():
    global collection

    collection = create_collection("pdf_collection", client)

    logger.debug("Reading PDF...")
    reader = read_pdf(pdf_path)
    if not reader:
        return

    logger.debug("Extratcting text from PDF...")
    pdf_text = extract_text_from_pdf(reader)

    logger.debug("Splinting text in chunks...")
    text_chunks = text_splitter(pdf_text)

    logger.debug("Adding chuncks to the database...")
    add_to_collection(text_chunks, collection)

    logger.info("Database populated with successfully!")


@app.on_event("shutdown")
def shutdown_event():
    global collection
    try:
        if collection:
            client.delete_collection("pdf_collection")
            logger.debug("Database clean up!")
    except Exception as ex:
        logger.error(f"Error in clean up the database: {ex}")
