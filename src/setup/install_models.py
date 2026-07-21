import requests

from src.ingestion.config.settings import OLLAMA_MODEL, OLLAMA_HOST


def pull_model(model: str, host: str):
    print(f"Downloading {model}...")

    response = requests.post(
        f"{host}/api/pull",
        json={
            "name": model,
        },
        stream=True,
    )

    response.raise_for_status()

    for line in response.iter_lines():
        if line:
            print(line.decode())


if __name__ == "__main__":
    pull_model(
        model=OLLAMA_MODEL,
        host=OLLAMA_HOST
    )

    # test installed model with ollama run model_name