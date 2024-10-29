from ..config import load_models_configs
from .type import DART_MODEL_TYPE


class LoadModelNode:
    DESCRIPTION = "Loads a Dart model."

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        configs = load_models_configs()
        return {
            "required": {
                "model_name": (list(configs.keys()),),
            },
        }

    RETURN_TYPES = (DART_MODEL_TYPE,)
    RETURN_NAMES = ("dart_model",)
    OUTPUT_TOOLTIPS = ("Dart model",)

    FUNCTION = "load_model"

    OUTPUT_NODE = False

    CATEGORY = "prompt/Danbooru Tags Transformer"

    def load_model(self, model_name: str):
        configs = load_models_configs()
        config = configs[model_name]
        model = config.load_model()
        return (model,)
