from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Literal, NamedTuple
from pathlib import Path
import logging
import re

from transformers import (
    GenerationConfig,
    PreTrainedTokenizerFast,
    ProcessorMixin,
)

from comfy.sd1_clip import escape_important, token_weights, unescape_important

from ..tags import estimate_rating, RATING_TYPE, load_tags


MODEL_VERSIONS = Literal["v2408"]


@dataclass
class PromptParseResult:
    rating: RATING_TYPE


class EncoderDecoderTokenizer(ProcessorMixin, ABC):
    encoder_tokenizer: PreTrainedTokenizerFast
    decoder_tokenizer: PreTrainedTokenizerFast


@dataclass
class AbstractTemplateConfig(ABC):
    pass


class ModelWrapper(ABC):
    """
    Wrapper class for dart models
    """

    version: MODEL_VERSIONS

    processor: EncoderDecoderTokenizer

    prompt_templates: dict[str, str]
    prompt_templates_default: dict[str, dict[str, str]]

    @abstractmethod
    def __init__(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def generate(
        self,
        text_prompt: str,
        tag_template: str,
        generation_config: GenerationConfig,
        **kwargs,
    ) -> tuple[str, str, str]:
        raise NotImplementedError

    @abstractmethod
    def format_prompt(self, template_name: str, format_kwargs: dict[str, str]) -> str:
        raise NotImplementedError

    def parse_prompt(self, prompt: str) -> PromptParseResult:
        tags = split_tokens(prompt)  # split by commas

        rating = estimate_rating(tags)

        return PromptParseResult(
            rating=rating,
        )

    def encode_ban_tags(self, ban_tags: str) -> list[list[int]] | None:
        # wildcard tags support
        tags = [tag.strip() for tag in ban_tags.split(",")]
        vocab = self.processor.decoder_tokenizer.get_vocab()

        ban_token_ids: list[list[int]] = []
        for tag in tags:  # search tags in vocab
            if "*" in tag:
                pattern = re.compile(tag.replace("*", ".*"))
                for token, _id in vocab.items():
                    if pattern.match(token):
                        ban_token_ids.append([_id])
            else:
                if tag in vocab:
                    ban_token_ids.append([vocab[tag]])

        if len(ban_token_ids) == 0:
            return None

        return ban_token_ids

    def search_tags(self, text: str, pattern: re.Pattern) -> str:
        result = pattern.search(text)
        if result is None:
            return ""
        tags = [tag.strip() for tag in result.group(1).split(",") if tag.strip()]
        return ", ".join(tags)

    @abstractmethod
    def extract_translation_result(self, raw_output: str) -> dict[str, str]:
        raise NotImplementedError

    @abstractmethod
    def extract_extension_result(self, raw_output: str) -> dict[str, str]:
        raise NotImplementedError


def unescape_important_all(text: str) -> list[str]:
    """
    Remove all emphasis brackets and returns a list of tokens
    """
    text = escape_important(text)
    parsed_weights: list[tuple[str, float]] = token_weights(text, 1.0)
    unescaped_tokens = []

    for part, _weight in parsed_weights:
        tokens = part.split(",")
        for token in tokens:
            pure_token = token.strip()
            if pure_token:
                unescaped_tokens.append(unescape_important(pure_token))

    return unescaped_tokens


def split_tokens(text: str, separator: str = ",") -> list[str]:
    """
    Split text into tokens without prefix and suffix spaces
    """
    return [token.strip() for token in text.split(separator) if token.strip()]
