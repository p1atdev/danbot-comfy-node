from ..models.utils import ModelWrapper
from ..models import v2408
from .type import DANBOT_MODEL_TYPE, DANBOT_CATEGORY, FORMAT_KWARGS_DTYPE

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

    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = (
        "text_prompt",
        "tag_template",
        "rating_tag",
        # "known_tags",
        # "unknown_tags",
    )
    OUTPUT_TOOLTIPS = (
        "Formatted prompt that should be passed to the upsampler node.",
        "The input tags.",
        "The rating tags detected from the input text.",
        # "Tags that the model knows except for copyright and character tags.",
        # "Tags that the model does not know.",
    )

    FUNCTION = "format"

    OUTPUT_NODE = False

    CATEGORY = DANBOT_CATEGORY


class V2408FormatterNode(FormatterNodeMixin):
    DESCRIPTION = "Formats a prompt for a Danbot-2408 model"

    EXPERIMENTAL = True

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model": (DANBOT_MODEL_TYPE,),
                "aspect_ratio": (
                    list(v2408.ASPECT_RATIO_MAP.keys()),
                    {
                        "default": "tall",
                    },
                ),
                "rating": (
                    ["auto"] + list(v2408.RATING_MAP.keys()),
                    {
                        "default": "general",
                    },
                ),
                "length": (
                    list(v2408.LENGTH_MAP.keys()),
                    {
                        "default": "very_short",
                    },
                ),
                "template_name": (
                    v2408.TEMPLATE_NAMES,
                    {
                        "default": "translation",
                    },
                ),
                "input_text": (
                    "STRING",
                    {
                        **INPUT_TAGS_OPTIONS,
                        "placeholder": "Natural language prompt. English and Japanese are supported.",
                    },
                ),
            },
            "optional": {
                "format_kwargs": (FORMAT_KWARGS_DTYPE,),
            },
        }

    def format(
        self,
        model: ModelWrapper,
        aspect_ratio: str,
        rating: str,
        length: str,
        template_name: str,
        input_text: str,
        format_kwargs: dict[str, str] = {},
    ):
        parsed = model.parse_prompt(input_text)

        rating_tag = v2408.RATING_MAP[parsed.rating if rating == "auto" else rating]

        default_kwargs = model.prompt_templates_default.get(template_name, {})
        template = model.format_prompt(
            template_name=template_name,
            format_kwargs={
                "aspect_ratio": v2408.ASPECT_RATIO_MAP[aspect_ratio],
                "rating": rating_tag,
                "length": v2408.LENGTH_MAP[length],
                **default_kwargs,
                **format_kwargs,
            },
        )

        return (
            input_text,
            template,
            parsed.rating,
        )
