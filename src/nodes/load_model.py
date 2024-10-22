from ..models import ALL_MODELS
from .type import DART_MODEL_TYPE


class LoadModelNode:
    DESCRIPTION = "Loads a Dart model."

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model_name": (list(ALL_MODELS.keys()),),
            },
        }

    RETURN_TYPES = (DART_MODEL_TYPE,)
    RETURN_NAMES = ("dart_model",)
    OUTPUT_TOOLTIPS = ("Dart model",)

    FUNCTION = "load_model"

    OUTPUT_NODE = False

    CATEGORY = "prompt/Danbooru Tags Transformer"

    def load_model(self, model_name: str):
        model_cls, config = ALL_MODELS[model_name]
        model = model_cls(**config)
        return (model,)
