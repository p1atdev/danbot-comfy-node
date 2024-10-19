from ..models.utils import ModelWrapper, normalize_tag_text
from ..models import v1, v2, v3
from .type import DART_MODEL_TYPE

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
                "model": (DART_MODEL_TYPE,),
                "rating": (
                    ["auto"] + list(v1.V1_RATING_MAP.keys()),
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
            },
        }

    def format(
        self,
        model: ModelWrapper,
        rating: str,
        length: str,
        copyright: str,
        character: str,
        input_tags: str,
    ):
        parsed = model.parse_prompt(input_tags, escape_brackets=False)

        copyright_tags = normalize_tag_text(", ".join([copyright, parsed.copyright]))
        character_tags = normalize_tag_text(", ".join([character, parsed.character]))
        condition_tags = parsed.known

        rating_tag = v1.V1_RATING_MAP[parsed.rating if rating == "auto" else rating]

        prompt = model.format_prompt(
            {
                "copyright": copyright_tags,
                "character": character_tags,
                "condition": condition_tags,
                "rating": rating_tag,
                "length": v1.V1_LENGTH_MAP[length],
            }
        )
        return (prompt,)


class V2FormatterNode(FormatterNodeMixin):
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model": (DART_MODEL_TYPE,),
                "aspect_ratio": (
                    list(v2.V2_ASPECT_RATIO_MAP.keys()),
                    {
                        "default": "tall",
                    },
                ),
                "rating": (
                    ["auto"] + list(v2.V2_RATING_MAP.keys()),
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
            },
        }

    def format(
        self,
        model: ModelWrapper,
        aspect_ratio: str,
        rating: str,
        length: str,
        identity: str,
        copyright: str,
        character: str,
        input_tags: str,
    ):
        parsed = model.parse_prompt(input_tags, escape_brackets=False)

        copyright_tags = normalize_tag_text(", ".join([copyright, parsed.copyright]))
        character_tags = normalize_tag_text(", ".join([character, parsed.character]))
        condition_tags = parsed.known

        rating_tag = v2.V2_RATING_MAP[parsed.rating if rating == "auto" else rating]

        prompt = model.format_prompt(
            {
                "copyright": copyright_tags,
                "character": character_tags,
                "condition": condition_tags,
                "aspect_ratio": v2.V2_ASPECT_RATIO_MAP[aspect_ratio],
                "rating": rating_tag,
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
                "model": (DART_MODEL_TYPE,),
                "aspect_ratio": (
                    list(v3.V3_ASPECT_RATIO_MAP.keys()),
                    {
                        "default": "tall",
                    },
                ),
                "rating": (
                    ["auto"] + list(v3.V3_RATING_MAP.keys()),
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
            },
        }

    def format(
        self,
        model: ModelWrapper,
        aspect_ratio: str,
        rating: str,
        length: str,
        copyright: str,
        character: str,
        input_tags: str,
    ):
        parsed = model.parse_prompt(input_tags, escape_brackets=False)

        copyright_tags = normalize_tag_text(", ".join([copyright, parsed.copyright]))
        character_tags = normalize_tag_text(", ".join([character, parsed.character]))
        condition_tags = parsed.known

        rating_tag = v3.V3_RATING_MAP[parsed.rating if rating == "auto" else rating]

        prompt = model.format_prompt(
            {
                "copyright": copyright_tags,
                "character": character_tags,
                "condition": condition_tags,
                "aspect_ratio": v3.V3_ASPECT_RATIO_MAP[aspect_ratio],
                "rating": rating_tag,
                "length": v3.V3_LENGTH_MAP[length],
            }
        )
        return (prompt,)
