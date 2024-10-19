from transformers import GenerationConfig

from ..models.utils import ModelWrapper
from ..models.v3 import V3_ASPECT_RATIO_MAP, V3_LENGTH_MAP, V3_RATING_MAP

STRING_OPTIONS = {
    "multiline": True,
    "lazy": True,
}


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
                        "placeholder": "vocaloid, ... (copyright tags)",
                    },
                ),
                "character": (
                    "STRING",
                    {
                        **STRING_OPTIONS,
                        "placeholder": "hatsune miku, ... (character tags)",
                    },
                ),
                "input_tags": (
                    "STRING",
                    {
                        **STRING_OPTIONS,
                        "placeholder": "1girl, solo, ... (general and meta tags)",
                    },
                ),
                "aspect_ratio": (
                    list(V3_ASPECT_RATIO_MAP.keys()),
                    {
                        "default": "tall",
                    },
                ),
                "rating": (
                    list(V3_RATING_MAP.keys()),
                    {
                        "default": "general",
                    },
                ),
                "length": (
                    list(V3_LENGTH_MAP.keys()),
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
                "aspect_ratio": V3_ASPECT_RATIO_MAP[aspect_ratio],
                "rating": V3_RATING_MAP[rating],
                "length": V3_LENGTH_MAP[length],
            }
        )
        return (prompt,)
