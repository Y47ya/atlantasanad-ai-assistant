from langchain_ollama import ChatOllama

from src.config.settings import OLLAMA_MODEL, OLLAMA_TEMPERATURE

llm = ChatOllama(
    model=OLLAMA_MODEL,
    temperature=OLLAMA_TEMPERATURE,
)