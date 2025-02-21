from transformers import GenerationConfig, set_seed

from ..models.utils import ModelWrapper
from .type import (
    DANBOT_MODEL_TYPE,
    DANBOT_GENERATION_CONFIG_TYPE,
    DANBOT_CATEGORY,
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


class GeneratorNode:
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
