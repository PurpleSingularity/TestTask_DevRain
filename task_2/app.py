"""
Task 2: Simple (non-RAG) recipe assistant.

This module builds small LangChain chains around a Google Gemini chat model to:
- generate cooking instructions for a given recipe title, and
- generate a required-ingredients list for a given recipe title.

Model:
Module uses Google Gemini chat model.
The best choice for this task is the Claude model,
as it excels at text analysis and is generally one of the most
powerful models currently available. However, I don't have access
to the Claude model, so I decided to use the second-best solution
(which has limited free access) – Google Gemini.
It's also worth noting that Task 2 doesn't yet use RAG,
meaning the model generates a response. OpenAI's GPT model
would be a better fit for these tasks, but it also doesn't have a free version,
and in Tasks 3-4, this script will be improved using RAG, so I decided to use Gemini.

Environment:
- Uses python-dotenv to load credentials/settings from .env (e.g., API key).

Warning!
For the script to work correctly, you must insert your Gemini API key into the ".env"
file in the following format:
```
GOOGLE_GEMINI_API_KEY=<your api key here>
```
"""

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from task_2.prompts import SYSTEM_PROMPT
from langchain_core.output_parsers import JsonOutputParser

# Load environment variables early so downstream SDKs can pick up configuration.
load_dotenv()

def cooking_instructions(title: str):
    """
        Generate step-by-step cooking instructions for a recipe.

        Args:
            title: Recipe name or a short description provided by the user.

        Returns:
            Parsed JSON produced by the model, as enforced by JsonOutputParser.
    """

    # Prompt is built as a system message (rules) + a human message (the user request).
    # In this solution, the question the model should answer is already included in the
    # prompt template, and all that remains is to substitute the necessary variables
    # from the system prompt and the user's request. Since, according to the task,
    # the user only provides the model with the title of the recipe, this is the simplest
    # way to generate the template. Alternatively, the question itself can also be passed
    # to the model separately. This approach will be demonstrated in Tasks 2 and 3.
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", f"""Generate cooking instructions for provided recipe 

        # Recipe:
        {title}""")
    ])

    # Deterministic output (temperature=0) helps JSON parsing stability.
    model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    # The parser expects the LLM to comply with the JSON protocol described in SYSTEM_PROMPT.
    parser = JsonOutputParser()
    chain = prompt | model | parser

    # Note: `title` is passed in variables even though the human message is already formatted;
    # keeping it allows easy refactors to a templated human message later.
    response = chain.invoke({"title": title})

    return response

def required_ingredients(title: str):
    """
        Generate a required-ingredients list for a recipe.

        Args:
            title: Recipe name or a short description provided by the user.

        Returns:
            Parsed JSON produced by the model, as enforced by JsonOutputParser.
    """

    # Same chain pattern as cooking_instructions(), but the request asks for ingredients instead of steps.
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", f"""Generate required ingredients for provided recipe 

        # Recipe:
        {title}""")
    ])

    model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    parser = JsonOutputParser()
    chain = prompt | model | parser

    response = chain.invoke({"title": title})

    return response
