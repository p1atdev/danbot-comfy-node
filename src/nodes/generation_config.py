from typing import Literal

from transformers import GenerationConfig

from .type import DANBOT_GENERATION_CONFIG_TYPE, DANBOT_CATEGORY


class GenerationConfigNode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "max_new_tokens": (
                    "INT",
                    {
                        "default": 256,
                        "min": 1,
                        "max": 512,
                        "step": 1,
                        "display": "number",
                        "tooltip": "Maximum number of tokens to generate",
                    },
                ),
                "do_sample": (
                    ["true", "false"],
                    {
                        "default": "true",
                        "tooltip": "Whether to use sampling or greedy decoding",
                    },
                ),
                "temperature": (
                    "FLOAT",
                    {
                        "default": 1.0,
                        "min": 0.1,
                        "max": 5.0,
                        "step": 0.05,
                        "display": "number",
                        "tooltip": (
                            "Temperature for sampling. "
                            "Lower values are more deterministic, higher values more random. "
                            "Default value is 1.0. Recommended to be less than 1.5."
                        ),
                    },
                ),
                "top_p": (
                    "FLOAT",
                    {
                        "default": 1.0,
                        "min": 0.1,
                        "max": 1.0,
                        "step": 0.1,
                        "display": "number",
                        "tooltip": (
                            "Tokens are sampled from the smallest set whose cumulative probability exceeds the probability p. "
                            "Default value is 1.0."
                        ),
                    },
                ),
                "top_k": (
                    "INT",
                    {
                        "default": 50,
                        "min": 10,
                        "max": 1000,
                        "step": 10,
                        "display": "number",
                        "tooltip": (
                            "Tokens are sampled from the top k most likely tokens. "
                            "Larger values mean more diversity and randomness. "
                            "Default value is 50. Recommended to be between 10 and 200."
                        ),
                    },
                ),
                "min_p": (
                    "FLOAT",
                    {
                        "default": 0.0,
                        "min": 0.0,
                        "max": 1.0,
                        "step": 0.05,
                        "display": "number",
                        "tooltip": (
                            "Minimum probability to select tokens from. "
                            "Tokens with probability less than this value are going to be ignored. "
                            "Default value is 0.00. If you set this value to around 0.1 ~ 0.2, "
                            "you can set higher temperature and top_k values."
                        ),
                    },
                ),
                "num_beams": (
                    "INT",
                    {
                        "default": 1,
                        "min": 1,
                        "max": 10,
                        "step": 1,
                        "display": "number",
                        "tooltip": (
                            "Number of beams to use for beam search. "
                            "1 means no beam search. It is effective when the temperature is too high. "
                            "Default value is 1."
                        ),
                    },
                ),
            }
        }

    RETURN_TYPES = (DANBOT_GENERATION_CONFIG_TYPE,)
    RETURN_NAMES = ("generation_config",)
    OUTPUT_TOOLTIPS = ("Generation config for the upsampler node.",)

    FUNCTION = "construct"

    OUTPUT_NODE = False

    CATEGORY = DANBOT_CATEGORY

    def construct(
        self,
        max_new_tokens: int,
        do_sample: Literal["true", "false"],
        temperature: float,
        top_p: float,
        top_k: int,
        min_p: float,
        num_beams: int,
    ):
        config = GenerationConfig(
            max_new_tokens=max_new_tokens,
            do_sample=do_sample == "true",
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            min_p=min_p,
            num_beams=num_beams,
            use_cache=True,
        )
        return (config,)
