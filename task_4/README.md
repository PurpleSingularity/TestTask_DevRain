# RAG Recipe Assistant API

RAG AI Assistant (FastAPI + Gemini + Qdrant).

## How to launch (Docker)

1. **Environment variables**:
   Paste your Google Gemini API key in `.env` file:
   
   ```env
   GOOGLE_API_KEY=<your API key>
   ```
   
2. **Launch**:
   Run the following commands from task_4 to start the application:
   
   ```bash
   docker build -t recipe-assistant .
   docker run -d -p 8000:8000 --env-file .env recipe-assistant
   ```
   
   The API will be accessible at `http://localhost:8000`.

3. **Test**:

   API can be tested using `curl` or by accessing the Swagger UI at `http://localhost:8000/docs`.   

   Run the following command to test the API by curl:
   
   ```bash
   curl -X 'POST' \
     'http://localhost:8000/chat' \
     -H 'accept: application/json' \
     -H 'Content-Type: application/json' \
     -d '{
     "history": [
       {
         "role": "user",
         "content": "content"
       }
     ]
   }'
   ```
   
   You should receive a response from the Gemini model.
4. Example of query:

```bash
   curl -X 'POST' \
  'http://localhost:8000/chat' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "history": [
    {
      "role": "user",
      "content": "i have milk, what can i cook?"
    }
  ]
}'
```

5. Example of response:

```bash
{
  "response": [
    {
      "title": "Ice Cream",
      "error": null,
      "recipe": "1. Beat with electric mixer.\n2. Put in freezer.",
      "ingredients": "2 eggs, 2 c sugar, 1 can Eagle brand milk, 1/2 pt cream, 2 tsp vanilla, pinch of salt, 2 qts milk",
      "NER": [
        "eggs",
        "sugar",
        "milk",
        "cream",
        "vanilla",
        "salt",
        "milk"
      ],
      "is_done": true
    },
    {
      "title": "Vanilla Ice Cream",
      "error": null,
      "recipe": "1. Combine sugar, eggs, evaporated milk and vanilla in large mixing bowl.\n2. Add enough milk to fill freezer 3/4 full.",
      "ingredients": "6 eggs, 1 1/2 c. sugar, 1 can evaporated milk, 1 Tbsp. milk, milk",
      "NER": [
        "eggs",
        "sugar",
        "milk",
        "milk",
        "milk"
      ],
      "is_done": true
    },
    {
      "title": "Easy Chocolate Frosting",
      "error": null,
      "recipe": "1. Bring sugar, butter and milk to a boil and boil 1 minute.\n2. Remove from stove and add chocolate chips and vanilla and beat. (Might need about 1/2 cup powdered sugar.)",
      "ingredients": "1 1/3 c. white sugar, 6 Tbsp. butter, 6 Tbsp. milk, 1/2 c. chocolate chips, 1/2 tsp. vanilla",
      "NER": [
        "white sugar",
        "butter",
        "milk",
        "chocolate chips",
        "vanilla"
      ],
      "is_done": true
    }
  ]
}
```

## Qdrant DB
Qdrant is used as a vector database.
DB is stored in `qdrant_db_local` folder.
Ensure that Qdrant DB is created before launching the API.
To create Qdrant DB, launch ingestion.py script.

## Testing from cli_test.py
1. Environment variables:

To test the Assistant from cli_test.py, put your API key in .env file in quotes.
```.env
GOOGLE_API_KEY="<your API key>"
```
2. Run cli_test.py

```bash
python cli_test.py
```