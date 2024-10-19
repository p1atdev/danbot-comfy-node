from ..models.utils import ModelWrapper
from ..models import v1, v2, v3

STRING_OPTIONS = {
    "multiline": True,
}

COPYRIGHT_PLACEHOLDER = "copyright tags (e.g. vocaloid, ...)"
CHARACTER_PLACEHOLDER = "character tags (e.g. hatsune miku, ...)"
INPUT_TAGS_PLACEHOLDER = "general and meta tags (e.g. 1girl, solo, ...)"


class FormatterNodeMixin:
    def __init__(self):
        pass

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("formatted_prompt",)

    FUNCTION = "format"

    OUTPUT_NODE = False

    CATEGORY = "prompt/Danbooru Tags Transformer"


class V1FormatterNode(FormatterNodeMixin):
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
                "rating": (
                    list(v1.V1_RATING_MAP.keys()),
                    {
                        "default": "general",
                    },
                ),
                "length": (
                    list(v1.V1_LENGTH_MAP.keys()),
                    {
                        "default": "long",
                    },
                ),
            },
        }

    def format(
        self,
        model: ModelWrapper,
        copyright: str,
        character: str,
        input_tags: str,
        rating: str,
        length: str,
    ):
        prompt = model.format_prompt(
            {
                "copyright": copyright,
                "character": character,
                "condition": input_tags,
                "rating": v1.V1_RATING_MAP[rating],
                "length": v1.V1_LENGTH_MAP[length],
            }
        )
        return (prompt,)


class V2FormatterNode(FormatterNodeMixin):
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


class V3FormatterNode(FormatterNodeMixin):
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
