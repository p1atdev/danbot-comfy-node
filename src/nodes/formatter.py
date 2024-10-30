from ..models.utils import ModelWrapper
from ..models import v1, v2, v3
from .type import DART_MODEL_TYPE

STRING_OPTIONS = {
    "multiline": True,
}

INPUT_TAGS_OPTIONS = {
    **STRING_OPTIONS,
    "placeholder": "input tags (e.g. 1girl, solo, hatsune miku, ...)",
    "tooltip": "Comma separated tags. This is the condition for upsampling tags. The copyright/character tags in this field are automatically detected.",
}


class FormatterNodeMixin:
    def __init__(self):
        pass

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = (
        "formatted_prompt",
        "input_tags",
        "copyright_tags",
        "character_tags",
        "known_tags",
        "unknown_tags",
    )
    OUTPUT_TOOLTIPS = (
        "Formatted prompt that should be passed to the upsampler node.",
        "The input tags.",
        "Tags that are categorized as copyright.",
        "Tags that are categorized as character.",
        "Tags that the model knows except for copyright and character tags.",
        "Tags that the model does not know.",
    )

    FUNCTION = "format"

    OUTPUT_NODE = False

    CATEGORY = "prompt/Danbooru Tags Transformer"


class V1FormatterNode(FormatterNodeMixin):
    DESCRIPTION = "Formats a prompt for a Dart v1 model. This node deos not compatible with the v2 and v3 models."

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
                "input_tags": (
                    "STRING",
                    {
                        **INPUT_TAGS_OPTIONS,
                    },
                ),
            },
        }

    def format(
        self,
        model: ModelWrapper,
        rating: str,
        length: str,
        input_tags: str,
    ):
        parsed = model.parse_prompt(input_tags, escape_brackets=False)

        rating_tag = v1.V1_RATING_MAP[parsed.rating if rating == "auto" else rating]

        prompt = model.format_prompt(
            {
                "copyright": parsed.copyright,
                "character": parsed.character,
                "condition": parsed.known,
                "rating": rating_tag,
                "length": v1.V1_LENGTH_MAP[length],
            }
        )
        return (
            prompt,
            input_tags,
            parsed.copyright,
            parsed.character,
            parsed.known,
            parsed.unknown,
        )


class V2FormatterNode(FormatterNodeMixin):
    DESCRIPTION = "Formats a prompt for a Dart v2 model. This node deos not compatible with the v1 and v3 models."

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
                "input_tags": (
                    "STRING",
                    {
                        **INPUT_TAGS_OPTIONS,
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
        input_tags: str,
    ):
        parsed = model.parse_prompt(input_tags, escape_brackets=False)

        rating_tag = v2.V2_RATING_MAP[parsed.rating if rating == "auto" else rating]

        prompt = model.format_prompt(
            {
                "copyright": parsed.copyright,
                "character": parsed.character,
                "condition": parsed.known,
                "aspect_ratio": v2.V2_ASPECT_RATIO_MAP[aspect_ratio],
                "rating": rating_tag,
                "length": v2.V2_LENGTH_MAP[length],
                "identity": v2.V2_IDENTITY_MAP[identity],
            }
        )
        return (
            prompt,
            input_tags,
            parsed.copyright,
            parsed.character,
            parsed.known,
            parsed.unknown,
        )


class V3FormatterNode(FormatterNodeMixin):
    DESCRIPTION = "Formats a prompt for a Dart v3 model. This node deos not compatible with the v1 and v2 models."

    EXPERIMENTAL = True

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
                "input_tags": (
                    "STRING",
                    {
                        **INPUT_TAGS_OPTIONS,
                        "placeholder": "general and meta tags (e.g. 1girl, solo, ...)",
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
        input_tags: str,
    ):
        parsed = model.parse_prompt(input_tags, escape_brackets=False)

        rating_tag = v3.V3_RATING_MAP[parsed.rating if rating == "auto" else rating]

        prompt = model.format_prompt(
            {
                "copyright": parsed.copyright,
                "character": parsed.character,
                "condition": parsed.known,
                "aspect_ratio": v3.V3_ASPECT_RATIO_MAP[aspect_ratio],
                "rating": rating_tag,
                "length": v3.V3_LENGTH_MAP[length],
            }
        )
        return (
            prompt,
            input_tags,
            parsed.copyright,
            parsed.character,
            parsed.known,
            parsed.unknown,
        )
