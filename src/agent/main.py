from src.agent.graph import graph


def main():

    result = graph.invoke(
        {
            "question": "Que couvre une RC Auto ?",
            "response": "",
        }
    )

    print(result)


if __name__ == "__main__":
    main()