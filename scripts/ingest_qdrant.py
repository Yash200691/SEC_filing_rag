from pathlib import Path
import json
import sys

from tqdm import tqdm

# -------------------------------------------------------
# Add Project Root to Python Path
# -------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

# -------------------------------------------------------
# Imports
# -------------------------------------------------------

from sentence_transformers import SentenceTransformer

from qdrant_client import QdrantClient

from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct
)

from config import (
    EMBEDDING_MODEL,
    QDRANT_URL,
    COLLECTION_NAME,
    VECTOR_SIZE,
    CHUNK_DIRECTORY,
    BATCH_SIZE
)

# =======================================================
# Load Embedding Model
# =======================================================

print("=" * 60)
print("Loading Embedding Model...")
print("=" * 60)

model = SentenceTransformer(EMBEDDING_MODEL)

print("Embedding Model Loaded.\n")

# =======================================================
# Connect to Qdrant
# =======================================================

print("=" * 60)
print("Connecting to Qdrant...")
print("=" * 60)

client = QdrantClient(url=QDRANT_URL)

print("Connected Successfully.\n")

# =======================================================
# Create Collection
# =======================================================

collections = client.get_collections().collections

collection_names = [c.name for c in collections]

if COLLECTION_NAME not in collection_names:

    client.create_collection(

        collection_name=COLLECTION_NAME,

        vectors_config=VectorParams(

            size=VECTOR_SIZE,

            distance=Distance.COSINE

        )

    )

    print(f"Collection '{COLLECTION_NAME}' Created.\n")

else:

    print(f"Collection '{COLLECTION_NAME}' Already Exists.\n")

# =======================================================
# Find Chunk Files
# =======================================================

chunk_dir = Path(CHUNK_DIRECTORY)

files = list(chunk_dir.rglob("*.json"))

print("=" * 60)
print(f"Found {len(files)} Chunk Files")
print("=" * 60)

# =======================================================
# Batch Upload
# =======================================================

point_id = 1

total_chunks = 0

for file in tqdm(files, desc="Processing Files"):

    with open(file, "r", encoding="utf-8") as f:

        chunks = json.load(f)

    # ---------------------------------------------------
    # Process chunks in batches
    # ---------------------------------------------------

    for start in range(0, len(chunks), BATCH_SIZE):

        batch = chunks[start:start + BATCH_SIZE]

        # -----------------------------------------------
        # Extract Texts
        # -----------------------------------------------

        texts = [chunk["text"] for chunk in batch]

        # -----------------------------------------------
        # Batch Embedding Generation
        # -----------------------------------------------

        embeddings = model.encode(

            texts,

            batch_size=BATCH_SIZE,

            normalize_embeddings=True,

            show_progress_bar=False

        )

        # -----------------------------------------------
        # Create Points
        # -----------------------------------------------

        points = []

        for chunk, embedding in zip(batch, embeddings):

            point = PointStruct(

                id=point_id,

                vector=embedding.tolist(),

                payload=chunk

            )

            points.append(point)

            point_id += 1

            total_chunks += 1

        # -----------------------------------------------
        # Upload Batch
        # -----------------------------------------------

        client.upsert(

            collection_name=COLLECTION_NAME,

            points=points

        )

# =======================================================
# Summary
# =======================================================

print("\n" + "=" * 60)
print("Indexing Completed Successfully!")
print("=" * 60)

print(f"Files Processed : {len(files)}")
print(f"Chunks Indexed  : {total_chunks}")
print(f"Collection      : {COLLECTION_NAME}")

print("=" * 60)