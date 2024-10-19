from typing import Literal


from transformers import GenerationConfig


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
                        "lazy": True,
                    },
                ),
                "do_sample": (
                    ["true", "false"],
                    {
                        "default": "true",
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
                        "lazy": True,
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
                        "lazy": True,
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
                        "lazy": True,
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
                        "lazy": True,
                    },
                ),
                "seed": (
                    "INT",
                    {
                        "default": 0,
                        "step": 1,
                        "display": "number",
                        "lazy": True,
                    },
                ),
            },
        }

    RETURN_TYPES = ("MODEL",)
    RETURN_NAMES = ("generation_config",)

    FUNCTION = "construct"

    OUTPUT_NODE = False

    CATEGORY = "prompt/Danbooru Tags Transformer"

    def check_lazy_status(
        self,
        max_new_tokens,
        do_sample,
        temperature,
        top_p,
        top_k,
        num_beams,
        seed,
    ):
        return [
            "max_new_tokens",
            "do_sample",
            "temperature",
            "top_p",
            "top_k",
            "num_beams",
            "seed",
        ]

    def construct(
        self,
        max_new_tokens: int,
        do_sample: Literal["true", "false"],
        temperature: float,
        top_p: float,
        top_k: int,
        num_beams: int,
        seed: int,  # comfyui backend does the all about seed in nice way
    ):
        config = GenerationConfig(
            max_new_tokens=max_new_tokens,
            do_sample=do_sample == "true",
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            num_beams=num_beams,
            use_cache=True,
        )
        return (config,)
