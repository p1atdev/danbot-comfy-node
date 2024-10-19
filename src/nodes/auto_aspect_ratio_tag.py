from typing import Literal
from abc import ABC, abstractmethod

from ..models import v2, v3


class AutoAspectRatioTagNodeMixin(ABC):
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
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

    # RETURN_TYPES = (
    #     list(v3.V3_ASPECT_RATIO_MAP.keys()),
    #     "INT",
    #     "INT",
    # )
    RETURN_NAMES = ("aspect_ratio_tag", "width", "height")

    FUNCTION = "calculate_aspect_ratio_tag"

    OUTPUT_NODE = False

    CATEGORY = "prompt/Danbooru Tags Transformer"

    def check_lazy_status(
        self,
        width,
        height,
    ):
        return [
            "width",
            "height",
        ]

    @abstractmethod
    def calculate_aspect_ratio_tag(
        self,
        width: int,
        height: int,
    ):
        raise NotImplementedError


class V2AutoAspectRatioTagNode(AutoAspectRatioTagNodeMixin):
    RETURN_TYPES = (
        list(v2.V2_ASPECT_RATIO_MAP.keys()),
        "INT",
        "INT",
    )

    def calculate_aspect_ratio_tag(
        self,
        width: int,
        height: int,
    ):
        return (v2.aspect_ratio_tag(width, height), width, height)


class V3AutoAspectRatioTagNode(AutoAspectRatioTagNodeMixin):
    RETURN_TYPES = (
        list(v3.V3_ASPECT_RATIO_MAP.keys()),
        "INT",
        "INT",
    )

    def calculate_aspect_ratio_tag(
        self,
        width: int,
        height: int,
    ):
        return (v3.aspect_ratio_tag(width, height), width, height)
