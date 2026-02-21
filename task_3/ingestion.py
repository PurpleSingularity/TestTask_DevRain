"""
Task 3 ingestion script: embed recipe.csv and store vectors in Qdrant.

Features:
- Loads CSV rows as payloads.
- Embeds a text representation of each row.
- Only title and NER are used for embedding because only this information is
commonly used by users to search for recipes.
- Upserts vectors + payloads into a local Qdrant collection.
- Persists progress to last_processed.txt for resumable ingestion.
- Sleeps between batches to reduce rate-limit risk.

Run this as a script (not imported as a library module).
"""

import os
import time
import uuid
from dotenv import load_dotenv

# Load environment variables.
load_dotenv()

from vector_db import QdrantStorage
from data_loader import load_and_chunk_data, embedding

# CSV input file path (relative to script working directory).
DATA_PATH = "recipe.csv"

# Load CSV as a list of dictionaries (rows).
chunks = load_and_chunk_data(DATA_PATH)
print(f"Total chunks: {len(chunks)}")

# Initialize storage once; reuse the same Qdrant client across all batches.
storage = QdrantStorage()

# Progress file allows resuming after an interruption (rate limits, crash, etc.).
PROGRESS_FILE = "last_processed.txt"

if os.path.exists(PROGRESS_FILE):
    with open(PROGRESS_FILE, "r") as f:
        start_index = int(f.read().strip())
    print(f"Resuming from index: {start_index}")
else:
    start_index = 0

# Batch size tuned for external embedding API throughput/limits.
batch_size = 20
try:
    for i in range(start_index, len(chunks), batch_size):
        try:
            batch = chunks[i:i + batch_size]
            print(f"Processing batch {i // batch_size + 1}...")

            # Convert each CSV row (dict) into a string to embed.
            texts_to_embed = [
                f"{row.get('title', '')}. NER: {row.get('NER', '')}"
                for row in batch
            ]
            vecs = embedding(texts_to_embed)

            # Store the raw CSV rows as payload for retrieval-time context building.
            payloads = batch

            # Generate unique IDs for Qdrant points.
            batch_ids = [str(uuid.uuid4()) for _ in range(len(batch))]

            # Persist vectors + payloads.
            storage.upsert(ids = batch_ids, vectors=vecs, payloads=payloads)

            # Save progress *after* a successful upsert so a restart resumes correctly.
            with open(PROGRESS_FILE, "w") as f:
                f.write(str(i + batch_size))

                # Small delay to reduce likelihood of hitting per-minute rate limits.
                time.sleep(1)

        except Exception as e:
            # Basic rate-limit handling by substring match.
            if "429" in str(e):
                print("Rate limit exceeded; waiting 60 seconds before retrying...")
                time.sleep(60)
            else:
                print(f"Error: {e}")
                break
finally:
    if 'storage' in globals():
        storage.client.close()

print("All data have been successfully embedded and saved!")