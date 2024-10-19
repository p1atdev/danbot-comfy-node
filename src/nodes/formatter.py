from transformers import GenerationConfig

from ..models.utils import ModelWrapper
from ..models import v2, v3

STRING_OPTIONS = {
    "multiline": True,
    "lazy": True,
}

COPYRIGHT_PLACEHOLDER = "copyright tags (e.g. vocaloid, ...)"
CHARACTER_PLACEHOLDER = "character tags (e.g. hatsune miku, ...)"
INPUT_TAGS_PLACEHOLDER = "general and meta tags (e.g. 1girl, solo, ...)"


class V2FormatterNode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model": ("MODEL",),
                "copyright": (
                    "STRING",
                    {
                        **STRING_OPTIONS,
                        "placeholder": COPYRIGHT_PLACEHOLDER,
                    },
                ),
                "character": (
                    "STRING",
                    {
                        **STRING_OPTIONS,
                        "placeholder": CHARACTER_PLACEHOLDER,
                    },
                ),
                "input_tags": (
                    "STRING",
                    {
                        **STRING_OPTIONS,
                        "placeholder": INPUT_TAGS_PLACEHOLDER,
                    },
                ),
                "aspect_ratio": (
                    list(v2.V2_ASPECT_RATIO_MAP.keys()),
                    {
                        "default": "tall",
                    },
                ),
                "rating": (
                    list(v2.V2_RATING_MAP.keys()),
                    {
                        "default": "general",
                    },
                ),
                "length": (
                    list(v2.V2_LENGTH_MAP.keys()),
                    {
                        "default": "medium",
                    },
                ),
                "identity": (
                    list(v2.V2_IDENTITY_MAP.keys()),
                    {
                        "default": "none",
                    },
                ),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("formatted_prompt",)

    FUNCTION = "format"

    OUTPUT_NODE = False

    CATEGORY = "prompt/Danbooru Tags Transformer"

    def check_lazy_status(
        self,
        model,
        copyright,
        character,
        input_tags,
        aspect_ratio,
        rating,
        length,
        identity,
    ):
        return [
            "model",
            "copyright",
            "character",
            "input_tags",
            "aspect_ratio",
            "rating",
            "length",
            "identity",
        ]

    def format(
        self,
        model: ModelWrapper,
        copyright: str,
        character: str,
        input_tags: str,
        aspect_ratio: str,
        rating: str,
        length: str,
        identity: str,
    ):
        prompt = model.format_prompt(
            {
                "copyright": copyright,
                "character": character,
                "condition": input_tags,
                "aspect_ratio": v2.V2_ASPECT_RATIO_MAP[aspect_ratio],
                "rating": v2.V2_RATING_MAP[rating],
                "length": v2.V2_LENGTH_MAP[length],
                "identity": v2.V2_IDENTITY_MAP[identity],
            }
        )
        return (prompt,)


class V3FormatterNode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model": ("MODEL",),
                "copyright": (
                    "STRING",
                    {
                        **STRING_OPTIONS,
                        "placeholder": COPYRIGHT_PLACEHOLDER,
                    },
                ),
                "character": (
                    "STRING",
                    {
                        **STRING_OPTIONS,
                        "placeholder": CHARACTER_PLACEHOLDER,
                    },
                ),
                "input_tags": (
                    "STRING",
                    {
                        **STRING_OPTIONS,
                        "placeholder": INPUT_TAGS_PLACEHOLDER,
                    },
                ),
                "aspect_ratio": (
                    list(v3.V3_ASPECT_RATIO_MAP.keys()),
                    {
                        "default": "tall",
                    },
                ),
                "rating": (
                    list(v3.V3_RATING_MAP.keys()),
                    {
                        "default": "general",
                    },
                ),
                "length": (
                    list(v3.V3_LENGTH_MAP.keys()),
                    {
                        "default": "medium",
                    },
                ),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("formatted_prompt",)

    FUNCTION = "format"

    OUTPUT_NODE = False

    CATEGORY = "prompt/Danbooru Tags Transformer"

    def check_lazy_status(
        self, model, copyright, character, input_tags, aspect_ratio, rating, length
    ):
        return [
            "model",
            "copyright",
            "character",
            "input_tags",
            "aspect_ratio",
            "rating",
            "length",
        ]

    def format(
        self,
        model: ModelWrapper,
        copyright: str,
        character: str,
        input_tags: str,
        aspect_ratio: str,
        rating: str,
        length: str,
    ):
        prompt = model.format_prompt(
            {
                "copyright": copyright,
                "character": character,
                "condition": input_tags,
                "aspect_ratio": v3.V3_ASPECT_RATIO_MAP[aspect_ratio],
                "rating": v3.V3_RATING_MAP[rating],
                "length": v3.V3_LENGTH_MAP[length],
            }
        )
        return (prompt,)
