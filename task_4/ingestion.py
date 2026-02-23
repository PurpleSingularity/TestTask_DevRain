"""
Task 4 ingestion script: embed recipe.csv and store vectors in Qdrant.
Similar to Task 3 ingestion.

This is functionally the same approach as Task 3 ingestion:
- reads CSV rows,
- embeds title+NER,
- upserts to Qdrant,
- stores progress in last_processed.txt.

Kept as a script intended to be run manually.
"""

import os
import time
import uuid
from dotenv import load_dotenv

load_dotenv()

from vector_db import QdrantStorage
from data_loader import load_and_chunk_data, embedding

DATA_PATH = "recipe.csv"

# Load data upfront so we know total size and can batch over it.
chunks = load_and_chunk_data(DATA_PATH)
print(f"Total chunks: {len(chunks)}")

storage = QdrantStorage()

PROGRESS_FILE = "last_processed.txt"

if os.path.exists(PROGRESS_FILE):
    with open(PROGRESS_FILE, "r") as f:
        start_index = int(f.read().strip())
    print(f"Resuming from index: {start_index}")
else:
    start_index = 0

batch_size = 20
try:
    for i in range(start_index, len(chunks), batch_size):
        try:
            batch = chunks[i:i + batch_size]
            print(f"Processing batch {i // batch_size + 1}...")
            texts_to_embed = [
                f"{row.get('title', '')}. NER: {row.get('NER', '')}"
                for row in batch
            ]
            vecs = embedding(texts_to_embed)

            # Store original dict rows as payload for later retrieval.
            payloads = batch

            # Assign unique IDs for each stored point.
            batch_ids = [str(uuid.uuid4()) for _ in range(len(batch))]
            storage.upsert(ids = batch_ids, vectors=vecs, payloads=payloads)

            # Persist progress so ingestion can resume without duplicating work.
            with open(PROGRESS_FILE, "w") as f:
                f.write(str(i + batch_size))

            time.sleep(1)

        except Exception as e:
            if "429" in str(e):
                print("Limit exceeded; waiting 60 seconds before retrying...")
                time.sleep(60)
            else:
                print(f"Error: {e}")
                break
finally:
    if 'store' in globals():
        storage.client.close()

print("All data have been successfully embedded and saved!")