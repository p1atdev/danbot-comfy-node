# from .v1 import V1_MODELS, V1Model
# from .v2 import V2_MODELS, V2Model
from .v3 import V3_MODELS, V3Model
from .utils import ModelWrapper

ALL_MODELS: dict[str, tuple[type[ModelWrapper], dict[str, str]]] = {
    **{name: (V3Model, config) for name, config in V3_MODELS.items()},
}
