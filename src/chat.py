from search import search_prompt

def main():
    ask = search_prompt()

    if not ask:
        print("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
        return

    print("Faça sua pergunta (digite 'sair' para encerrar):\n")
    while True:
        question = input("PERGUNTA: ").strip()
        if question.lower() in ["sair", "exit", "quit"]:
            print("Encerrando o chat.")
            break
        answer = ask(question)
        print(f"RESPOSTA: {answer}\n")

if __name__ == "__main__":
    main()