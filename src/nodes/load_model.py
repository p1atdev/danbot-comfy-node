from ..models import ALL_MODELS


class LoadModelNode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model_name": (list(ALL_MODELS.keys()),),
            },
        }

    RETURN_TYPES = ("MODEL",)
    RETURN_NAMES = ("dart_model",)

    FUNCTION = "load_model"

    OUTPUT_NODE = False

    CATEGORY = "prompt/Danbooru Tags Transformer"

    def check_lazy_status(self, model_name):
        return ["model_name"]

    def load_model(self, model_name: str):
        model_cls, config = ALL_MODELS[model_name]
        model = model_cls(**config)
        return (model,)
