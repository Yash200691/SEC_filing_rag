from retriever.embedding import EmbeddingModel
embedder = EmbeddingModel()

vector = embedder.encode(

    "What are Apple's risks?"

)

print(len(vector))

print(vector[:10])