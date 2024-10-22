from transformers import GenerationConfig, set_seed

from ..models.utils import ModelWrapper
from .type import DART_MODEL_TYPE, DART_GENERATION_CONFIG_TYPE


class UpsamplerNode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "dart_model": (DART_MODEL_TYPE,),
                "formatted_prompt": (
                    "STRING",
                    {
                        "forceInput": True,
                        "tooltip": "Formatted prompt that will be passed to the dart model to upsample tags",
                    },
                ),
                "generation_config": (
                    DART_GENERATION_CONFIG_TYPE,
                    {
                        "tooltip": "Generation configuration for the upmsapling tags",
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
                "negative_prompt": (
                    "STRING",
                    {
                        "forceInput": True,
                        "tooltip": "Negative prompt that prevents to generate tags that are not wanted",
                    },
                ),
            },
        }

    RETURN_TYPES = (
        "STRING",
        "STRING",
    )
    RETURN_NAMES = (
        "generated_tags",
        "raw_output",
    )
    OUTPUT_TOOLIPS = (
        "The generated tags by the model. This does not include the input prompt.",
        "The raw output of the model. This includes the all prompt and special tags.",
    )

    FUNCTION = "upsample"

    OUTPUT_NODE = False

    CATEGORY = "prompt/Danbooru Tags Transformer"

    def check_lazy_status(
        self,
        dart_model,
        formatted_prompt,
        generation_config,
        seed,
        **kwargs,
    ):
        return [
            "dart_model",
            "formatted_prompt",
            "generation_config",
            "seed",
        ]

    def upsample(
        self,
        dart_model: ModelWrapper,
        formatted_prompt: str,
        generation_config: GenerationConfig,
        seed: int,
        negative_prompt: str | None = None,
    ):
        set_seed(seed)
        _full, new, raw = dart_model.generate(
            formatted_prompt,
            generation_config,
            negative_prompt=negative_prompt,
        )

        return (new, raw)
