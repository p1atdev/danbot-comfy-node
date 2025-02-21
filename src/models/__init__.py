from .v2408 import V2408Model
from .utils import ModelWrapper, MODEL_VERSIONS

MODEL_VERSION_TO_CLASS: dict[MODEL_VERSIONS, type[ModelWrapper]] = {
    "v2408": V2408Model,
}
