import logging
import os
import chromadb
import getpass
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import Chroma
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from pdf_reader import read_pdf, extract_text_from_pdf
from chunking_strategy import invoke_text_spliter
from chromadb_function import create_collection, add_to_collection
from langchain.embeddings.openai import OpenAIEmbeddings

logger = logging.getLogger(__name__)

load_dotenv()

if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPEN_API_KEY"] = getpass.getpass("Enter API key for OpenAI: ")

app = Flask(__name__)

chat_model = ChatOpenAI(model="gpt-4", api_key=os.environ["OPENAI_API_KEY"])

client = chromadb.PersistentClient("./mycollection")

embedding_function = OpenAIEmbeddings()


def process_pdf_and_query(pdf_filename, collection_name):
    pdf_path = os.path.join("./pdfs", pdf_filename)

    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"The file {pdf_filename} not found.")

    reader = read_pdf(pdf_path)
    pdf_content = extract_text_from_pdf(reader)

    text_chunks = invoke_text_spliter(
        separators=["\n\n", "\n", " ", ". ", " "],
        chunk_size=2000,
        chunk_overlap=250,
        content=pdf_content
    )

    collection = create_collection(collection_name, client)
    add_to_collection(text_chunks, collection=collection)

    chroma_db = Chroma(
        persist_directory="./mycollection",
        embedding_function=embedding_function
    )
    chroma_db.add_texts(text_chunks)
    retriever = chroma_db.as_retriever()

    return retriever


@app.route("/read_pdf", methods=["POST"])
def text_ai():
    pdf_file = request.files.get("pdf_file")
    user_question = request.form.get("text")

    if not pdf_file or not user_question:
        return jsonify({"error": "PDF filename or text not provided"}), 400

    try:
        pdf_filename = pdf_file.filename
        pdf_path = os.path.join("./pdfs", pdf_filename)

        pdf_file.save(pdf_path)

        retriever = process_pdf_and_query(pdf_filename, collection_name="pdf_collection")
        qa_chain = RetrievalQA.from_chain_type(
            llm=chat_model,
            retriever=retriever,
            chain_type="stuff"
        )

        response = qa_chain.run(user_question)
        return jsonify({"response": response})

    except FileNotFoundError as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
