import requests

from src.config.settings import OLLAMA_MODEL, OLLAMA_HOST, OLLAMA_TEMPERATURE, OLLAMA_PULL_IF_MISSING, OLLAMA_PROVIDER
from src.llm.base_llm import BaseLLM


class OllamaLLM(BaseLLM):

    def __init__(
        self,
        model: str,
        provider: str,
        host: str,
        pull_if_missing: str,
        temperature: float = 0.0
    ):
        self._provider = provider
        self._model = model
        self._host = host
        self._temperature = temperature
        self.pull_if_missing = pull_if_missing
        self.ensure_model()

    @property
    def provider(self) -> str:
        return self._provider

    @property
    def model(self) -> str:
        return self._model

    def ensure_model(self):

        response = requests.get(f"{self._host}/api/tags")
        response.raise_for_status()

        installed = {
            model["name"]
            for model in response.json()["models"]
        }

        if self.model in installed:
            print(f"{self.model} already installed")
            return

        if not self.pull_if_missing:
            raise RuntimeError(
                f"{OLLAMA_MODEL} is not installed.\n Use python src/setup/install_models.py."
            )

        print(f"Pulling {self._model}...")

        response = requests.post(
            f"{self._host}/api/pull",
            json={"name": self._model},
            timeout=None,
            stream=True,
        )

        response.raise_for_status()

        # Consume the stream until download finishes
        for _ in response.iter_lines():
            pass

    def generate(self, prompt: str) -> str:

        response = requests.post(
            f"{self._host}/api/generate",
            json={
                "model": self._model,
                "prompt": prompt,
                "stream": False,
            },
        )

        response.raise_for_status()

        return response.json()["response"].strip()


# llm = OllamaLLM(
#     model=OLLAMA_MODEL,
#     provider=OLLAMA_PROVIDER,
#     host=OLLAMA_HOST,
#     pull_if_missing=OLLAMA_PULL_IF_MISSING,
#     temperature=OLLAMA_TEMPERATURE
# )
#
# answer = llm.generate("Hello!")
#
# print(answer)