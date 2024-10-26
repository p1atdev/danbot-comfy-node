from typing import Literal
import os
from pathlib import Path

RATING_TYPE = Literal["general", "sensitive", "questionable", "explicit"]

EXPLICIT_TAGS = ["explicit"]
QUESTIONABLE_TAGS = ["nsfw", "questionable"]
SENSITIVE_TAGS = ["sensitive"]
GENERAL_TAGS = ["safe", "general"]


SELF_PATH_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
TAGS_ROOT_DIR = SELF_PATH_DIR / ".." / "tags"


def estimate_rating(tags: list[str]) -> RATING_TYPE:
    for tag in tags:
        if tag in EXPLICIT_TAGS:
            return "explicit"
        if tag in QUESTIONABLE_TAGS:
            return "questionable"
        if tag in SENSITIVE_TAGS:
            return "sensitive"
    return "general"


def load_tags(path: str | Path) -> list[str]:
    with open(path, "r") as f:
        tags = f.read().splitlines()

    # remove comment out with "//"
    tags = [tag.split("//")[0] for tag in tags if not tag.startswith("//")]

    # remove empty lines
    tags = [tag for tag in tags if tag]

    return tags


def normalize_tag_text(text: str, separator: str = ", ") -> str:
    """
    Normalize tag text by removing extra spaces and joining tokens
    """
    return separator.join(
        [token.strip().replace("_", " ") for token in text.split(",") if token.strip()]
    )
