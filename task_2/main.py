"""
Task 2 CLI entrypoint. Needed only to show examples of app.py usage

A small interactive loop that lets a user pick a mode:
- generate cooking instructions
- generate required ingredients
- stop the program

s required in the task, this script prints model raw output, however,
it is parsed as JSON so it can be easily converted to a structured output.
"""

from task_2.app import cooking_instructions, required_ingredients

# Main REPL-like loop flag.
stop = False
while not stop:
    # User menu shown on every iteration.
    print("""What should i do? 
    Type "C" - for cooking instructions. 
    Type "I" - for ingredients. 
    Type "S" - for stop.""")

    mode = input('Mode: ')

    # user mode inout is formatted lowercase to ensure case-insensitivity.
    if mode.lower().strip() == 'c':
        title = input('Generate cooking instructions for: ')
        raw_output = cooking_instructions(title = title)
        print(raw_output)
    elif mode.lower().strip() == 'i':
        title = input('Generate required ingredients for: ')
        raw_output = required_ingredients(title = title)
        print(raw_output)
    elif mode.lower().strip() == 's':
        stop = True
    else:
        print('Invalid input. Please type "C" or "I" or "S"')

    # Spacer line to keep the CLI readable.
    print('')