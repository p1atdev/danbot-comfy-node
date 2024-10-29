from .v1 import V1Model
from .v2 import V2Model
from .v3 import V3Model
from .utils import ModelWrapper, MODEL_VERSIONS

MODEL_VERSION_TO_CLASS: dict[MODEL_VERSIONS, type[ModelWrapper]] = {
    "v1": V1Model,
    "v2": V2Model,
    "v3": V3Model,
}
