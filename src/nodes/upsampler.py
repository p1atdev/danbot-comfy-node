from transformers import GenerationConfig, set_seed

from ..models.utils import ModelWrapper
from .type import (
    DANBOT_MODEL_TYPE,
    DANBOT_GENERATION_CONFIG_TYPE,
    DANBOT_CATEGORY,
    FORMAT_KWARGS_DTYPE,
)

UPSAMPLER_INPUT_TYPES = {
    "required": {
        "danbot_model": (DANBOT_MODEL_TYPE,),
        "text_prompt": (
            "STRING",
            {
                "forceInput": True,
                "tooltip": "Natural language prompt. English and Japanese are supported.",
            },
        ),
        "tag_template": (
            "STRING",
            {
                "forceInput": True,
                "tooltip": "Formatted tag template that will be passed to the danbot model to upsample tags",
            },
        ),
        "seed": (
            "INT",
            {
                "default": 0,
                "step": 1,
                "min": 0,
                "max": 2**32 - 1,
                "display": "number",
            },
        ),
    },
    "optional": {
        "stop_token": (
            "STRING",
            {
                "default": "</general>",
                "tooltip": "Stop token to stop generation",
            },
        ),
        "ban_tags": (
            "STRING",
            {
                "forceInput": True,
                "tooltip": "Tags to ban during generation",
            },
        ),
        "generation_config": (
            DANBOT_GENERATION_CONFIG_TYPE,
            {
                "tooltip": "Generation configuration for the upmsapling tags",
            },
        ),
    },
}


class UpsamplerNode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return UPSAMPLER_INPUT_TYPES

    RETURN_TYPES = (
        "STRING",
        "STRING",
    )
    RETURN_NAMES = (
        "generated_tags",
        "raw_output",
    )
    OUTPUT_TOOLIPS = (
        "The generated tags by the model.",
        "The raw output of the model. This includes the special tokens.",
    )

    FUNCTION = "upsample"

    OUTPUT_NODE = False

    CATEGORY = DANBOT_CATEGORY

    def upsample(
        self,
        danbot_model: ModelWrapper,
        text_prompt: str,
        tag_template: str,
        seed: int,
        stop_token: str | None = "</general>",
        ban_tags: str | None = None,
        generation_config: GenerationConfig = GenerationConfig(
            do_sample=False,
        ),
    ):
        set_seed(seed)
        _full, new, raw = danbot_model.generate(
            text_prompt=text_prompt,
            tag_template=tag_template,
            generation_config=generation_config,
            ban_tags=ban_tags,
            stop_token=stop_token,
        )

        return (new, raw)


class TranslatorNode(UpsamplerNode):
    @classmethod
    def INPUT_TYPES(s):
        input_types = UPSAMPLER_INPUT_TYPES.copy()
        input_types["optional"]["stop_token"] = (
            "STRING",
            {
                "default": "</translation>",
                "tooltip": "Stop token to stop generation",
            },
        )

        return input_types

    RETURN_TYPES = (
        "STRING",
        "STRING",
        FORMAT_KWARGS_DTYPE,
    )
    RETURN_NAMES = (
        "translated_tags",
        "raw_output",
        "translation_kwargs",
    )
    OUTPUT_TOOLIPS = (
        "The translated tags by the model.",
        "The raw output of the model. This includes the special tokens.",
        "The translation result as a dict",
    )

    FUNCTION = "translate"

    def translate(
        self,
        danbot_model: ModelWrapper,
        text_prompt: str,
        tag_template: str,
        seed: int,
        stop_token: str | None = "</translation>",
        ban_tags: str | None = None,
        generation_config: GenerationConfig = GenerationConfig(
            do_sample=False,
        ),
    ):
        set_seed(seed)
        _full, new, raw = danbot_model.generate(
            text_prompt=text_prompt,
            tag_template=tag_template,
            generation_config=generation_config,
            ban_tags=ban_tags,
            stop_token=stop_token,
        )
        translation = danbot_model.extract_translation_result(raw)

        return (new, raw, translation)


class ExtenderNode(UpsamplerNode):
    @classmethod
    def INPUT_TYPES(s):
        input_types = UPSAMPLER_INPUT_TYPES.copy()
        input_types["optional"]["stop_token"] = (
            "STRING",
            {
                "default": "</extension>",
                "tooltip": "Stop token to stop generation",
            },
        )

        return input_types

    RETURN_TYPES = (
        "STRING",
        "STRING",
        FORMAT_KWARGS_DTYPE,
    )
    RETURN_NAMES = (
        "extended_tags",
        "raw_output",
        "extension_kwargs",
    )
    OUTPUT_TOOLIPS = (
        "The extended tags by the model.",
        "The raw output of the model. This includes the special tokens.",
        "The extension result as a dict",
    )

    FUNCTION = "extend"

    def extend(
        self,
        danbot_model: ModelWrapper,
        text_prompt: str,
        tag_template: str,
        seed: int,
        stop_token: str | None = "</extension>",
        ban_tags: str | None = None,
        generation_config: GenerationConfig = GenerationConfig(
            do_sample=False,
        ),
    ):
        set_seed(seed)
        _full, new, raw = danbot_model.generate(
            text_prompt=text_prompt,
            tag_template=tag_template,
            generation_config=generation_config,
            ban_tags=ban_tags,
            stop_token=stop_token,
        )
        extension = danbot_model.extract_extension_result(raw)

        return (new, raw, extension)
