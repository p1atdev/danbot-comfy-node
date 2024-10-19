from typing import Literal

RATING_TYPE = Literal["general", "sensitive", "questionable", "explicit"]

EXPLICIT_TAGS = ["explicit"]
QUESTIONABLE_TAGS = ["nsfw", "questionable"]
SENSITIVE_TAGS = ["sensitive"]
GENERAL_TAGS = ["safe", "general"]


def estimate_rating(tags: list[str]) -> RATING_TYPE:
    for tag in tags:
        if tag in EXPLICIT_TAGS:
            return "explicit"
        if tag in QUESTIONABLE_TAGS:
            return "questionable"
        if tag in SENSITIVE_TAGS:
            return "sensitive"
    return "general"
