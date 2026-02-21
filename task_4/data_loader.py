"""
Task 4 data loading + embedding utilities.
Similar to Task 3.

Responsibilities:
- Load recipe data from a CSV file into a list of dictionaries (one per row).
- Embed a list of strings into vectors using Gemini embedding model.

Notes:
- .env is loaded at import time so the embedding client can pick up credentials.
- Commented-out text splitting is preserved as-is.
"""

import csv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
# from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Instantiate the embedding model
EMBEDDING_MODEL = GoogleGenerativeAIEmbeddings(model = "models/gemini-embedding-001")

def load_and_chunk_data(file_path):
    """
    Load a CSV file and return its rows as dictionaries.

    Args:
        file_path: Path to the CSV file (UTF-8).

    Returns:
        List[dict]: Each dict is a CSV row keyed by column name.
    """
    with open(file_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        chunks = list(reader)

    # Optional splitting.
    #text_splitter = RecursiveCharacterTextSplitter(
    #   chunk_size=1000,  # Adjust the chunk size as needed
    #   chunk_overlap=200  # Adjust the overlap for better context
    #)
    #chunks = text_splitter.split_documents(data)

    return chunks

def embedding(chunks: list[str]) -> list[list[float]]:
    """
    Embed a list of text chunks into vectors.

    Args:
        chunks: List of strings to embed.

    Returns:
        List of embedding vectors aligned with the input order.
    """
    # embed_documents returns one vector per input string.
    response = EMBEDDING_MODEL.embed_documents(chunks)
    return response