from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Literal
import os
from pathlib import Path
import logging

from transformers import GenerationConfig, PreTrainedTokenizerBase

from comfy.sd1_clip import escape_important, token_weights, unescape_important
from ..tags import estimate_rating, RATING_TYPE


MODEL_VERSIONS = Literal["v1", "v2", "v3"]

SELF_PATH_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
TAGS_ROOT_DIR = SELF_PATH_DIR / ".." / "tags"


def load_tags(path: str | Path) -> list[str]:
    with open(path, "r") as f:
        tags = f.read().splitlines()

    return tags


@dataclass
class PromptParseResult:
    copyright: str
    character: str
    known: str
    unknown: str
    rating: RATING_TYPE


class ModelWrapper(ABC):
    """
    Wrapper class for dart models
    """

    version: MODEL_VERSIONS

    copyright_tags_path: str | Path
    character_tags_path: str | Path

    tokenizer: PreTrainedTokenizerBase

    @abstractmethod
    def __init__(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def generate(
        self, prompt: str, generation_config: GenerationConfig, **kwargs
    ) -> tuple[str, str, str]:
        raise NotImplementedError

    @abstractmethod
    def format_prompt(self, format_kwargs: dict[str, str]) -> str:
        raise NotImplementedError

    def parse_prompt(self, prompt: str, escape_brackets: bool) -> PromptParseResult:
        copyright_list = load_tags(self.copyright_tags_path)
        character_list = load_tags(self.character_tags_path)
        vocab_list = list(self.tokenizer.get_vocab().keys())
        special_list = self.tokenizer.all_special_tokens

        if escape_brackets:
            tags = unescape_important_all(prompt)  # remove (brackets:1.5)
        else:
            tags = split_tokens(prompt)  # split by commas

        found_copyright_tags = []
        found_character_tags = []
        found_known_tags = []
        unknown_tags = []

        for tag in tags:
            if tag in copyright_list:
                found_copyright_tags.append(tag)
            if tag in character_list:
                found_character_tags.append(tag)

            if tag in special_list:
                logging.warning(f"Special tag found: {tag} (skipped)")
            elif tag not in vocab_list:
                logging.warning(f"Unknown tag found: {tag} (skipped)")
                unknown_tags.append(tag)
            else:
                found_known_tags.append(tag)

        rating = estimate_rating(unknown_tags)

        return PromptParseResult(
            copyright=", ".join(found_copyright_tags),
            character=", ".join(found_character_tags),
            known=", ".join(found_known_tags),
            unknown=", ".join(unknown_tags),
            rating=rating,
        )


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


def normalize_tag_text(text: str, separator: str = ",") -> str:
    """
    Normalize tag text by removing extra spaces and joining tokens
    """
    return separator.join(
        [token.strip() for token in text.split(separator) if token.strip()]
    )
