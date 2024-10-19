from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Literal

from transformers import GenerationConfig


class ModelWrapper(ABC):
    """
    Wrapper class for dart models
    """

    @abstractmethod
    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def generate(
        self, prompt: str, generation_config: GenerationConfig, **kwargs
    ) -> str:
        pass

    @abstractmethod
    def format_prompt(self, format_kwargs: dict[str, str]) -> str:
        pass
