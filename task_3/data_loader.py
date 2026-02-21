"""
Task 3 data loading + embedding utilities.

Responsibilities:
- Load recipe rows from a CSV into Python dictionaries.
- Convert a list of strings into embeddings using Gemini embedding model.

Note:
- This module loads .env at import time so embedding clients can read credentials.
"""

import csv
from langchain_community.document_loaders import CSVLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
# from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the embedding model once; reuse across calls to avoid re-instantiation overhead.
EMBEDDING_MODEL = GoogleGenerativeAIEmbeddings(model = "models/gemini-embedding-001")

def load_and_chunk_data(file_path):
    """
    Load a CSV file into a list of row dictionaries.

    Args:
        file_path: Path to a UTF-8 CSV file.

    Returns:
        List[dict]: Each dict is a row with column names as keys.
    """
    with open(file_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        chunks = list(reader)

    # Optional text splitting.
    #text_splitter = RecursiveCharacterTextSplitter(
    #   chunk_size=1000,  # Adjust the chunk size as needed
    #   chunk_overlap=200  # Adjust the overlap for better context
    #)
    #chunks = text_splitter.split_documents(data)

    return chunks

def embedding(chunks: list[str]) -> list[list[float]]:
    """
    Embed multiple text chunks into vectors.

    Args:
        chunks: List of strings to embed.

    Returns:
        List of vectors (list[float]) corresponding to each input string.
    """
    # embed_documents returns vectors aligned with input order.
    response = EMBEDDING_MODEL.embed_documents(chunks)
    return response