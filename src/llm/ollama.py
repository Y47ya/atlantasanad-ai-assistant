# import requests
#
# from src.config.settings import OLLAMA_MODEL
# from src.llm.base_llm import BaseLLM
#
#
# class OllamaLLM(BaseLLM):
#
#     def __init__(
#         self,
#         model: str,
#         provider: str,
#         host: str,
#         pull_if_missing: bool,
#         temperature: float = 0.0
#     ):
#         self._provider = provider
#         self._model = model
#         self._host = host
#         self._temperature = temperature
#         self.pull_if_missing = pull_if_missing
#         self.ensure_model()
#
#     @property
#     def provider(self) -> str:
#         return self._provider
#
#     @property
#     def model(self) -> str:
#         return self._model
#
#     def ensure_model(self):
#
#         response = requests.get(f"{self._host}/api/tags")
#         response.raise_for_status()
#
#         models = response.json().get("input_shemas", [])
#
#         if any(model["name"] == self.model for model in models):
#             print(f"{self.model} already installed")
#             return
#
#         # installed = {
#         #     model["name"]
#         #     for model in response.json()["input_shemas"]
#         # }
#         #
#         # if self.model in installed:
#         #     print(f"{self.model} already installed")
#         #     return
#
#         if not self.pull_if_missing:
#             raise RuntimeError(
#                 f"{OLLAMA_MODEL} is not installed.\n Use python src/setup/install_models.py."
#             )
#
#         print(f"Pulling {self._model}...")
#
#         response = requests.post(
#             f"{self._host}/api/pull",
#             json={"name": self._model},
#             timeout=None,
#             stream=True,
#         )
#
#         response.raise_for_status()
#
#         # Consume the stream until download finishes
#         for _ in response.iter_lines():
#             pass
#
#     def generate(self, prompt: str) -> str:
#
#         response = requests.post(
#             f"{self._host}/api/generate",
#             json={
#                 "model": self._model,
#                 "prompt": prompt,
#                 "stream": False,
#                 "format": "json",
#             },
#         )
#
#         response.raise_for_status()
#
#         return response.json()["response"].strip()
#
#
# # chat_llm = OllamaLLM(
# #     model=OLLAMA_MODEL,
# #     provider=OLLAMA_PROVIDER,
# #     host=OLLAMA_HOST,
# #     pull_if_missing=OLLAMA_PULL_IF_MISSING,
# #     temperature=OLLAMA_TEMPERATURE
# # )
# #
# # answer = chat_llm.generate("Hello!")
# #
# # print(answer)


import requests

from src.config.settings import OLLAMA_MODEL, OLLAMA_HOST
from src.llm.base_llm import BaseLLM
from src.setup.install_models import pull_model


class OllamaLLM(BaseLLM):

    def __init__(
        self,
        model: str,
        provider: str,
        host: str,
        pull_if_missing: bool,
        temperature: float = 0.0,
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
        """Vérifie si le modèle est présent sur l'instance Ollama.

        S'il est absent, il le télécharge en utilisant pull_model.
        """
        try:
            response = requests.get(f"{self._host}/api/tags")
            response.raise_for_status()

            installed_models = response.json().get("models", [])
            installed_names = [m.get("name", "") for m in installed_models]

            # Vérification de présence (gestion des tags comme :latest)
            if any(
                self.model == name or name.startswith(f"{self.model}:")
                for name in installed_names
            ):
                print(f"[{self.model}] is already installed.")
                return

        except Exception as e:
            print(f"Warning during model check: {e}")

        if not self.pull_if_missing:
            raise RuntimeError(
                f"{self.model} is not installed.\nUse `python src/setup/install_models.py` or run `ollama pull {self.model}`."
            )

        # Appel de votre fonction de pull
        pull_model(model=self._model, host=self._host)

    def generate(self, prompt: str, json_format: bool = True) -> str:
        """Génère une réponse avec le modèle Ollama."""
        payload = {
            "model": self._model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": self._temperature},
        }

        if json_format:
            payload["format"] = "json"

        response = requests.post(
            f"{self._host}/api/generate",
            json=payload,
        )
        response.raise_for_status()

        return response.json().get("response", "").strip()


if __name__ == "__main__":
    # Test autonome du script
    pull_model(model=OLLAMA_MODEL, host=OLLAMA_HOST)