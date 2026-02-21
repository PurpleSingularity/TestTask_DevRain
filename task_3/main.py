"""
Task 3 CLI entrypoint (RAG version).

Provides an interactive loop for:
- cooking instructions (RAG)
- ingredients list (RAG)
- recipe recommendations by ingredients (RAG)
"""

from app import rag_cooking_instructions, rag_required_ingredients, recommend_recipes

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
        print(*raw_output)
    elif mode.lower().strip() == 'i':
        title = input('Generate required ingredients for: ')
        raw_output = rag_required_ingredients(title = title)
        print(*raw_output)
    elif mode.lower().strip() == 'r':
        # Split on comma+space to match expected user input format like: "egg, milk, flour"
        ingredients = input('Find recipes for your ingredients: ').split(", ")
        raw_output = recommend_recipes(ingredients = ingredients)
        print(*raw_output)
    elif mode.lower().strip() == 's':
        stop = True
    else:
        print('Invalid input. Please type "C" or "I" or "S"')

    print('')