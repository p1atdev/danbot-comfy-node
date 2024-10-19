from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Literal

from transformers import GenerationConfig

MODEL_VERSIONS = Literal["v1", "v2", "v3"]


class ModelWrapper(ABC):
    """
    Wrapper class for dart models
    """

    version: MODEL_VERSIONS

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
