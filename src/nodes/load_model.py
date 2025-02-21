from ..config import load_models_configs
from .type import DANBOT_MODEL_TYPE, DANBOT_CATEGORY


class LoadModelNode:
    DESCRIPTION = "Loads a Danbot model."

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

    RETURN_TYPES = (DANBOT_MODEL_TYPE,)
    RETURN_NAMES = ("danbot_model",)
    OUTPUT_TOOLTIPS = ("Danbot model",)

    FUNCTION = "load_model"

    OUTPUT_NODE = False

    CATEGORY = DANBOT_CATEGORY

    def load_model(self, model_name: str):
        configs = load_models_configs()
        config = configs[model_name]
        model = config.load_model()
        return (model,)
