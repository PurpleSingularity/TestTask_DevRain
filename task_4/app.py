"""
Task 4: FastAPI wrapper around the RAG recipe assistant.

Exposes a single POST /chat endpoint that:
- accepts conversation history,
- infers user intent (instructions / ingredients / recommendations),
- calls the corresponding RAG function,
- returns the model output.

This file is the HTTP/API layer; the retrieval and generation live in rag_logic.py.
"""

from typing import List, Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

# Import RAG functions.
from rag_logic import rag_cooking_instructions, rag_required_ingredients, recommend_recipes

app = FastAPI(title="RAG Recipe Assistant API")

# Request/response schemas
class Message(BaseModel):
    """One chat message in the conversation history."""
    role: str
    content: str

class ChatRequest(BaseModel):
    """Incoming request containing full message history (last message must be user)."""
    history: List[Message]

class ChatResponse(BaseModel):
    """Outgoing response wrapper (keeps API output stable even if internal format changes)."""
    response: Any

def detect_intent(text: str):
    """
    Detect user intent from the input text using a simple heuristic.
    In a more robust version, this could be an LLM classifier or a ruleset with regexes.
    """
    t = text.lower()
    if any(word in t for word in ["how to cook", "instructions", "how can i cook", "recipe for"]):
        return "instructions"
    elif any(word in t for word in ["ingredients", "what do i need", "what is in"]):
        return "ingredients"
    else:
        return "recommend"


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat endpoint.

    Contract:
    - history must be non-empty
    - last message must have role == "user"
    """
    if not request.history:
        raise HTTPException(status_code=400, detail="History cannot be empty")

    last_msg = request.history[-1]
    if last_msg.role != "user":
        raise HTTPException(status_code=400, detail="Last message must be from user")

    user_query = last_msg.content
    intent = detect_intent(user_query)

    try:
        if intent == "instructions":
            # Extract potential title from common phrasing so retrieval is more focused.
            title = user_query.lower().replace("how to cook", "").replace("how can i cook", "").strip("? ")
            result = rag_cooking_instructions(title if title else user_query)

        elif intent == "ingredients":
            # Similar extraction for ingredient questions; fall back to original query if empty.
            title = user_query.lower().replace("what ingredients do i need for", "").strip("? ")
            result = rag_required_ingredients(title if title else user_query)

        else:
            # Treat the query as a (comma-separated) list of ingredients.
            ingredients_list = [i.strip() for i in user_query.replace("I have", "").split(",") if i.strip()]
            result = recommend_recipes(ingredients_list)

        return ChatResponse(response=result)

    except Exception as e:
        # Any unexpected exception is converted to HTTP 500 so the client receives a structured error.
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    # Local dev server entrypoint.
    uvicorn.run(app, host="0.0.0.0", port=8000)
