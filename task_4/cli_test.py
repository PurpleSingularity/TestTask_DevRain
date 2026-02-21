"""
Task 4 CLI test client.

A quick manual test harness for rag_logic.py without running the FastAPI server.
Useful for debugging retrieval/generation in isolation.
"""

from rag_logic import rag_cooking_instructions, rag_required_ingredients, recommend_recipes

stop = False
while not stop:
    print("""What should i do? 
    Type "C" - for me to provide cooking instructions for your meal. 
    Type "I" - for me to provide ingredients for your meal. 
    Type "R" - for me to provide 3 recipes for your ingredients.
    Type "S" - for stop.""")

    mode = input('Mode: ')

    if mode.lower().strip() == 'c':
        title = input('Generate cooking instructions for: ')
        raw_output = rag_cooking_instructions(title = title)
        # Raw output is expected to be list-like; star-unpacking prints items separated by spaces.
        print(*raw_output)
    elif mode.lower().strip() == 'i':
        title = input('Generate required ingredients for: ')
        raw_output = rag_required_ingredients(title = title)
        print(*raw_output)
    elif mode.lower().strip() == 'r':
        ingredients = input('Find recipes for your ingredients: ').split(", ")
        raw_output = recommend_recipes(ingredients = ingredients)
        print(*raw_output)
    elif mode.lower().strip() == 's':
        stop = True
    else:
        print('Invalid input. Please type "C" or "I" or "S"')

    print('')