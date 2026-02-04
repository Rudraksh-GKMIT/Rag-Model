from src.llm.rag.pipline import rag_model

def main():
    query = input("Welcome to the Rag model\nEnter the question: ")
    while True:
        answer = rag_model(query=query)
        print("\n[Rag Model]: ",answer)
        query=input("\n[Your Response]: ").strip()
        if query.lower() == "/bye":
            break


if __name__ =="__main__" :
    main()
