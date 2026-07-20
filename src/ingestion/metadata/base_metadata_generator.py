from abc import ABC, abstractmethod


class MetadataGenerator(ABC):

    @abstractmethod
    def generate(self):
        pass