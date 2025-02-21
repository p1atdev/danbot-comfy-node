from ..models.utils import ModelWrapper
from ..models import v2408
from .type import (
    DANBOT_MODEL_TYPE,
    DANBOT_CATEGORY,
    FORMAT_KWARGS_DTYPE,
    TEMPLATE_CONFIG_DTYPE,
)

STRING_OPTIONS = {
    "multiline": True,
}

INPUT_TAGS_OPTIONS = {
    **STRING_OPTIONS,
    "placeholder": "input tags (e.g. 1girl, solo, hatsune miku, ...)",
    "tooltip": "Comma separated tags. This is the condition for upsampling tags. The copyright/character tags in this field are automatically detected.",
}


class TemplateConfigNode:
    def __init__(self):
        pass

    RETURN_TYPES = (TEMPLATE_CONFIG_DTYPE, "STRING")
    RETURN_NAMES = (
        "template_config",
        "template_name",
    )
    OUTPUT_TOOLTIPS = (
        "The template config.",
        "The template name.",
    )

    FUNCTION = "get_template"

    OUTPUT_NODE = False

    CATEGORY = DANBOT_CATEGORY


class V2408TemplateConfigNode(TemplateConfigNode):
    DESCRIPTION = "Formats a prompt for a Danbot-2408 model"

    EXPERIMENTAL = True

    RETURN_TYPES = (TEMPLATE_CONFIG_DTYPE, v2408.TEMPLATE_NAMES)

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
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
            },
            "optional": {
                "format_kwargs": (FORMAT_KWARGS_DTYPE,),
            },
        }

    def get_template(
        self,
        aspect_ratio: str,
        rating: str,
        length: str,
        template_name: v2408.TEMPLATE_NAME,
    ):
        config = v2408.TemplateConfig(
            aspect_ratio=aspect_ratio,
            rating=rating,
            length=length,
        )

        return (config, template_name)


class FormatterNodeMixin:
    def __init__(self):
        pass

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("tag_template",)
    OUTPUT_TOOLTIPS = (
        "Formatted tag template that should be passed to the upsampler node.",
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
                "template_config": (
                    TEMPLATE_CONFIG_DTYPE,
                    {},
                ),
                "template_name": (
                    v2408.TEMPLATE_NAMES,
                    {
                        "forceInput": True,
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
        template_config: v2408.TemplateConfig,
        template_name: v2408.TEMPLATE_NAME,
        format_kwargs: dict[str, str] = {},
    ):
        default_kwargs = model.prompt_templates_default.get(template_name, {})
        template = model.format_prompt(
            template_name=template_name,
            format_kwargs={
                "aspect_ratio": v2408.ASPECT_RATIO_MAP[template_config.aspect_ratio],
                "rating": v2408.RATING_MAP[template_config.rating],
                "length": v2408.LENGTH_MAP[template_config.length],
                **default_kwargs,
                **format_kwargs,
            },
        )

        return (template,)
