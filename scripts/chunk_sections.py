from pathlib import Path
import json
import nltk
import tiktoken

print("Imports completed")

nltk.download("punkt")
print("Punkt downloaded")

MAX_TOKENS = 512
OVERLAP_SENTENCES = 2

INPUT_DIR = Path("data/sections")
OUTPUT_DIR = Path("data/chunks")

print("Input directory:", INPUT_DIR.resolve())

files = list(INPUT_DIR.rglob("*.json"))

print(f"Found {len(files)} JSON files")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Tokenizer (same tokenizer family used by many OpenAI models)
tokenizer = tiktoken.get_encoding("cl100k_base")


def count_tokens(text):
    return len(tokenizer.encode(text))


def create_chunks(text):

    sentences = nltk.sent_tokenize(text)

    chunks = []
    current_chunk = []
    current_tokens = 0

    for sentence in sentences:

        sentence_tokens = count_tokens(sentence)

        if sentence_tokens > MAX_TOKENS:
            continue

        if current_tokens + sentence_tokens > MAX_TOKENS:

            if current_chunk:
                chunks.append(" ".join(current_chunk))

            overlap = (
                current_chunk[-OVERLAP_SENTENCES:]
                if len(current_chunk) >= OVERLAP_SENTENCES
                else current_chunk
            )

            current_chunk = overlap.copy()
            current_tokens = count_tokens(" ".join(current_chunk))

        current_chunk.append(sentence)
        current_tokens += sentence_tokens

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


files = list(INPUT_DIR.rglob("*.json"))

for file in files:

    with open(file, "r", encoding="utf-8") as f:
        sections = json.load(f)

    output = []

    chunk_number = 1

    for section_name, text in sections.items():

        chunks = create_chunks(text)

        for chunk in chunks:

            output.append({
                "chunk_id": chunk_number,
                "section": section_name,
                "text": chunk
            })

            chunk_number += 1

    relative = file.relative_to(INPUT_DIR)

    output_file = OUTPUT_DIR / relative

    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4)

print("Chunking Complete!")