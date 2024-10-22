from typing import Literal

from transformers import GenerationConfig

from .type import DART_GENERATION_CONFIG_TYPE


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
                        "default": 0.9,
                        "min": 0.1,
                        "max": 5.0,
                        "step": 0.05,
                        "display": "number",
                        "tooltip": "Temperature for sampling. Lower values are more deterministic, higher values more random",
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
                        "tooltip": "Tokens are sampled from the smallest set whose cumulative probability exceeds the probability p",
                    },
                ),
                "top_k": (
                    "INT",
                    {
                        "default": 50,
                        "min": 0,
                        "max": 1000,
                        "step": 10,
                        "display": "number",
                        "tooltip": "Tokens are sampled from the top k most likely tokens",
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
                        "tooltip": "Number of beams to use for beam search. 1 means no beam search. It is effective when the temperature is high",
                    },
                ),
                # "repetition_penalty": (
                #     "FLOAT",
                #     {
                #         "default": 1.0,
                #         "min": 1.0,
                #         "max": 2.0,
                #         "step": 0.1,
                #         "display": "number",
                #         "tooltip": "The parameter for repetition penalty. 1.0 means no penalty",
                #     },
                # ),
            },
        }

    RETURN_TYPES = (DART_GENERATION_CONFIG_TYPE,)
    RETURN_NAMES = ("generation_config",)
    OUTPUT_TOOLTIPS = ("Generation config for the upsampler node.",)

    FUNCTION = "construct"

    OUTPUT_NODE = False

    CATEGORY = "prompt/Danbooru Tags Transformer"

    def construct(
        self,
        max_new_tokens: int,
        do_sample: Literal["true", "false"],
        temperature: float,
        top_p: float,
        top_k: int,
        num_beams: int,
        # repetition_penalty: float,
    ):
        config = GenerationConfig(
            max_new_tokens=max_new_tokens,
            do_sample=do_sample == "true",
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            num_beams=num_beams,
            use_cache=True,
            guidance_scale=1.5,
            # repetition_penalty=repetition_penalty,
        )
        return (config,)
