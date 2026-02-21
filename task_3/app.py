"""
Task 3: RAG recipe assistant.

This module:
- embeds a user question,
- retrieves relevant recipe records from Qdrant (vector search),
- formats the retrieved payloads into a context block,
- calls a Gemini chat model with a RAG prompt, and
- parses the response as JSON.

Embedding model:
- Gemini embedding is best suited to work with Gemini AI model

Retriving strategy:
- RAG data embbedings are stored in Qdrant storage.
- RAG data embedding and ingesting explained in ingestion.py.
- Retrieval strategy is based on nearest neighbor search.
- Module get user query (Recipe title or ingredients list), embed it and search for nearest
neighbours in Qdrant storage.
- As cooking requires precise ingredients, the retrieval strategy prioritizes recipes with closest
embedding vectors to the query.
- From users query only recipe title (or ingredients list) is embedded and used for retrieval to
provide more relevant results.
- Only suitable fields from payload are recived and included in the context block to avoid
excessive data transfer:
    - title and recipe for cooking instructions,
    - title and ingredients list for ingredients recommendation and
    - title, ingredients and recipe for recipe recommendations.

Note:
- A single QdrantStorage instance is created at import time for reuse because of gemini
embedding limited usage. New storage can be created using ingestion.py.

Warning!
For the script to work correctly, you must insert your Gemini API key into the ".env"
file in the following format:
```
GOOGLE_GEMINI_API_KEY=<your api key here>
```
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from data_loader import embedding
from vector_db import QdrantStorage
from prompts import RAG_PROMPT
from dotenv import load_dotenv
from langchain_core.output_parsers import JsonOutputParser

# Load environment variables.
load_dotenv()
# Reuse a single storage client across calls to avoid reconnect overhead.
store = QdrantStorage()

def search_db(question, top_k: int = 3):
    """
       Vector-search the database for items relevant to the question.

       Args:
           question: User query string.
           top_k: How many nearest neighbors to retrieve.

       Returns:
           A list of Qdrant points (objects with .payload, etc.).
    """

    # embedding() returns a list of vectors; we embed a single query and take the first.
    query_vector = embedding([question])[0]
    search_result = store.search(query_vector, top_k)
    return search_result

def form_context(question, top_k: int = 3, needed_contexts = None):
    """
        Build a markdown-ish context string from retrieved Qdrant payloads.

        Args:
            question: User query used for retrieval.
            top_k: How many records to retrieve.
            needed_contexts: Which payload fields to include in the context. If None, defaults to:
            - title,
            - ingredients,
            - recipe and
            - NER

        Returns:
            A string block combining relevant fields from each retrieved recipe.
    """

    if needed_contexts is None:
        # Default payload fields expected in recipe.csv / ingestion payloads.
        needed_contexts = ["title", "ingredients", "recipe", "NER"]

    search_result = search_db(question, top_k)
    recipe_blocks = []

    for relevant in search_result:
        payload = relevant.payload
        parts = []
        for field in needed_contexts:
            # Empty fields checked separately to avoid exceptions.
            value = payload.get(field, "No information")
            parts.append(f"**{field}:** {value}")

        # Join fields with line breaks.
        recipe_blocks.append("\n".join(parts))

    # Join blocks with separator.
    context_block = "\n\n ---- \n\n".join(recipe_blocks)
    return context_block

def rag_cooking_instructions(title: str):
    """
        Generate cooking instructions using RAG.

        Args:
            title: Recipe name (or query) used to retrieve and to ask the model.

        Returns:
            Parsed JSON response from the model.
    """

    prompt = RAG_PROMPT
    question = f"How can I cook {title}"

    # context retrieval uses `title` (not the full question string), which is a design choice to
    # get more relevant results.
    context = form_context(question = title, top_k= 3, needed_contexts = ["title", "recipe"])

    model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    parser = JsonOutputParser()

    chain = prompt | model | parser

    # Chain expects `context` and `question` keys (see prompts.py template variables).
    response = chain.invoke({"context": context, "question": question})

    return response

def rag_required_ingredients(title: str):
    """
        Generate required ingredients using RAG.

        Args:
            title: Recipe name (or query) used to retrieve and to ask the model.

        Returns:
            Parsed JSON response from the model.
    """

    prompt = RAG_PROMPT
    question = f"What ingredients do I need to cook {title}"
    context = form_context(question = title, top_k= 3, needed_contexts = ["title", "ingredients"] )

    model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    parser = JsonOutputParser()
    chain = prompt | model | parser

    response = chain.invoke({"context": context, "question": question})

    return response

def recommend_recipes(ingredients: list[str]):
    """
       Recommend recipes based on a list of ingredients using RAG.

       Args:
           ingredients: List of ingredients (strings).

       Returns:
           Parsed JSON response from the model (recommendations).
   """

    prompt = RAG_PROMPT
    # Convert list into a single query string for retrieval and prompting.
    ingredients = ', '.join(ingredients)

    # In this prompt, we ask for 3 recipes or less, if there are not enough recipes found.
    # task stated, that model must find "N" recipes, but how "N" is recived is not specified, so
    # in this case i assume that N=3. "N" value can be easily changed in prompt template or even
    # stated as global variable in "prompt.py" if needed.
    question = f"What 3 (or less if you can't find 3) recipes I can cook using these ingredients: {ingredients}"
    context = form_context(question = ingredients, top_k= 5, needed_contexts = ["title", "ingredients", "recipe"])

    model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", temperature=0)
    parser = JsonOutputParser()
    chain = prompt | model | parser

    response = chain.invoke({"context": context, "question": question})

    return response
