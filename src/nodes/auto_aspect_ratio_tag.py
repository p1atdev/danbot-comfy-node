from typing import Literal

from ..models import v3
from ..models.v3 import V3_ASPECT_RATIO_MAP


class AutoAspectRatioTagNode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model_type": (
                    ["v3"],
                    {
                        "default": "v3",
                    },
                ),
                "width": (
                    "INT",
                    {
                        "default": 832,
                        "step": 32,
                        "force_input": True,
                    },
                ),
                "height": (
                    "INT",
                    {
                        "default": 1152,
                        "step": 32,
                        "force_input": True,
                    },
                ),
            },
        }

    RETURN_TYPES = (
        list(V3_ASPECT_RATIO_MAP.keys()),
        "INT",
        "INT",
    )
    RETURN_NAMES = ("aspect_ratio_tag", "width", "height")

    FUNCTION = "calculate_aspect_ratio_tag"

    OUTPUT_NODE = False

    CATEGORY = "prompt/Danbooru Tags Transformer"

    def check_lazy_status(
        self,
        model_type,
        width,
        height,
    ):
        return [
            "model_type",
            "width",
            "height",
        ]

    def calculate_aspect_ratio_tag(
        self,
        model_type: Literal["v3"],
        width: int,
        height: int,
    ):
        # if model_type == "v2":
        #     return (v2.aspect_ratio_tag(width, height), width, height)
        if model_type == "v3":
            return (v3.aspect_ratio_tag(width, height), width, height)
