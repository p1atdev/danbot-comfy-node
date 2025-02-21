from abc import ABC, abstractmethod

from ..models import v2408
from .type import DANBOT_CATEGORY


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

    RETURN_NAMES = ("aspect_ratio_tag", "width", "height")

    FUNCTION = "calculate_aspect_ratio_tag"

    OUTPUT_NODE = False

    CATEGORY = DANBOT_CATEGORY

    @abstractmethod
    def calculate_aspect_ratio_tag(
        self,
        width: int,
        height: int,
    ):
        raise NotImplementedError


class V2408AutoAspectRatioTagNode(AutoAspectRatioTagNodeMixin):
    DESCRIPTION = (
        "Calculates the aspect ratio tag of an image to generate by v2408 rule."
    )

    EXPERIMENTAL = True

    RETURN_TYPES = (
        list(v2408.ASPECT_RATIO_MAP.keys()),
        "INT",
        "INT",
    )
    OUTPUT_TOOLTIPS = ("Aspect ratio tag for v2408 model", "Width", "Height")

    def calculate_aspect_ratio_tag(
        self,
        width: int,
        height: int,
    ):
        return (v2408.aspect_ratio_tag(width, height), width, height)
