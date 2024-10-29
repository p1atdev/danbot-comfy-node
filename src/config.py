import os
from pathlib import Path
import yaml
from dataclasses import dataclass

from .models import (
    ModelWrapper,
    MODEL_VERSIONS,
    MODEL_VERSION_TO_CLASS,
)

SELF_PATH_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
CONFIG_ROOT_DIR = SELF_PATH_DIR / ".." / "config"

MODELS_CONFIG_FILE_PATH = CONFIG_ROOT_DIR / "models.yml"
PROMPT_TEMPLATE_CONFIG_FILE_PATH = CONFIG_ROOT_DIR / "prompt_templates.yml"


@dataclass
class ModelConfig:
    version: MODEL_VERSIONS
    prompt_template_id: str

    data: dict[str, str]

    def load_model(self) -> ModelWrapper:
        model_cls = MODEL_VERSION_TO_CLASS[self.version]
        prompt_templates = load_prompt_templates()
        prompt_template = prompt_templates[self.prompt_template_id]
        return model_cls(prompt_template=prompt_template, **self.data)


# id: str pair
PromptTemplates = dict[str, str]


def load_models_configs() -> dict[str, ModelConfig]:
    with open(MODELS_CONFIG_FILE_PATH, "r") as file:
        models_configs: list[dict] = yaml.safe_load(file)

    return {
        model_config.pop("name"): ModelConfig(
            version=model_config.pop("version"),
            prompt_template_id=model_config.pop("prompt_template_id"),
            data=model_config,
        )
        for model_config in models_configs
    }


def load_prompt_templates() -> PromptTemplates:
    with open(PROMPT_TEMPLATE_CONFIG_FILE_PATH, "r") as file:
        config: dict[str, str] = yaml.safe_load(file)

    # remove all newlines
    return {id: template.replace("\n", "") for id, template in config.items()}
