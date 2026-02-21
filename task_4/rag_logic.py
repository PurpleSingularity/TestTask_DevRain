"""
Task 4: RAG logic (retrieval + prompting + JSON parsing).

This is the same core idea as Task 3, used by:
- the FastAPI app (app.py), and/or
- the CLI tester (cli_test.py).

Flow:
1) embed the query
2) retrieve relevant payloads from Qdrant
3) format a context block
4) call Gemini with a RAG prompt
5) parse response into JSON
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from data_loader import embedding
from vector_db import QdrantStorage
from prompts import RAG_PROMPT
from dotenv import load_dotenv
from langchain_core.output_parsers import JsonOutputParser

load_dotenv()
store = QdrantStorage()

def search_db(question, top_k: int = 3):
    """
   Search the vector database for context relevant to `question`.

   Args:
       question: User query string.
       top_k: Number of nearest results to return.

   Returns:
       List of Qdrant points (each includes payload).
   """
    query_vector = embedding([question])[0]
    search_result = store.search(query_vector, top_k)
    return search_result

def form_context(question, top_k: int = 3, needed_contexts = None):
    """
    Create the context block supplied to the LLM from retrieved payload fields.

    Args:
        question: Query used to retrieve relevant records.
        top_k: Retrieval size.
        needed_contexts: Payload keys to include in the context (defaults to common recipe fields).

    Returns:
        A single string that concatenates fields for each retrieved item.
    """

    if needed_contexts is None:
        needed_contexts = ["title", "ingredients", "recipe", "NER"]

    search_result = search_db(question, top_k)
    recipe_blocks = []

    for relevant in search_result:
        payload = relevant.payload
        parts = []
        for field in needed_contexts:
            value = payload.get(field, "No information")
            parts.append(f"**{field}:** {value}")

        recipe_blocks.append("\n".join(parts))

    context_block = "\n\n ---- \n\n".join(recipe_blocks)
    return context_block

def rag_cooking_instructions(title: str):
    """
    Produce cooking instructions using retrieval-augmented generation.

    Args:
        title: Recipe name/query.

    Returns:
        Parsed JSON response.
    """

    prompt = RAG_PROMPT
    question = f"How can I cook {title}"
    context = form_context(question = title, top_k= 3, needed_contexts = ["title", "recipe"])

    model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    parser = JsonOutputParser()

    chain = prompt | model | parser

    response = chain.invoke({"context": context, "question": question})

    return response

def rag_required_ingredients(title: str):
    """
    Produce required ingredients using retrieval-augmented generation.

    Args:
        title: Recipe name/query.

    Returns:
        Parsed JSON response.
    """

    prompt = RAG_PROMPT
    question = f"What ingredients do I need to cook {title}"
    context = form_context(question = title, top_k= 3 )

    model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    parser = JsonOutputParser()
    chain = prompt | model | parser

    response = chain.invoke({"context": context, "question": question})

    return response

def recommend_recipes(ingredients: list[str]):
    """
    Recommend up to 3 recipes based on provided ingredients.

    Args:
        ingredients: List of ingredients.

    Returns:
        Parsed JSON response.
    """

    prompt = RAG_PROMPT
    ingredients = ', '.join(ingredients)
    question = f"What 3 (or less if you can't find 3) recipes I can cook using these ingredients: {ingredients}"
    context = form_context(question = ingredients, top_k= 5 )

    model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", temperature=0)
    parser = JsonOutputParser()
    chain = prompt | model | parser

    response = chain.invoke({"context": context, "question": question})

    return response
