from retriever.RAGPipeline import RAGPipeline

pipeline = RAGPipeline()

while True:

    question = input("\nAsk: ")

    if question.lower() == "exit":
        break

    answer = pipeline.ask(question)

    print("\nAnswer:\n")

    print(answer)