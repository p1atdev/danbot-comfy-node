from typing import Literal
import math

import torch

from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    MistralForCausalLM,
    PreTrainedTokenizerBase,
    PreTrainedTokenizer,
    GenerationConfig,
)
from optimum.onnxruntime.modeling_decoder import ORTModelForCausalLM

from .utils import (
    ModelWrapper,
    TAGS_ROOT_DIR,
)

V3_RATING_MAP = {
    "general": "<|rating:general|>",
    "sensitive": "<|rating:sensitive|>",
    "questionable": "<|rating:questionable|>",
    "explicit": "<|rating:explicit|>",
}

V3_LENGTH_MAP = {
    "very_short": "<|length:very_short|>",
    "short": "<|length:short|>",
    "medium": "<|length:medium|>",
    "long": "<|length:long|>",
    "very_long": "<|length:very_long|>",
}

V3_ASPECT_RATIO_MAP = {
    "too_tall": "<|aspect_ratio:too_tall|>",
    "tall_wallpaper": "<|aspect_ratio:tall_wallpaper|>",
    "tall": "<|aspect_ratio:tall|>",
    "square": "<|aspect_ratio:square|>",
    "wide": "<|aspect_ratio:wide|>",
    "wide_wallpaper": "<|aspect_ratio:wide_wallpaper|>",
    "too_wide": "<|aspect_ratio:too_wide|>",
}

PROMPT_TEMPLATE_SFT = (
    "<|bos|>"
    "{rating}{aspect_ratio}{length}"
    "<copyright>{copyright}</copyright>"
    "<character>{character}</character>"
    "<general>{condition}<|input_end|>"
).strip()

PROMPT_TEMPLATE_USE = (
    "<|bos|>"
    "{rating}{aspect_ratio}{length}"
    "<copyright>{copyright}</copyright>"
    "<character>{character}</character>"
    "<use>{condition}</use>"
    "<general><|input_end|>"
    "<group>{condition}</group>"
).strip()

PROMPT_TEMPLATE_PRETRAIN = (
    "<|bos|>"
    "{rating}{aspect_ratio}{length}"
    "<copyright>{copyright}</copyright>"
    "<character>{character}</character>"
    "<general>{condition}"
).strip()

INPUT_END = "<|input_end|>"

V3_MODELS: dict[str, dict[str, str]] = {
    # "v3 241006-sft (eager)": {
    #     "model_name_or_repo_id": "p1atdev/dart-v3-llama-8L-241005_241006-sft",
    #     "model_type": "eager",
    #     "prompt_template": "sft"
    # },
    # "v3 241008-sft-fix (eager)": {
    #     "model_name_or_repo_id": "p1atdev/dart-v3-llama-8L-241005_241008-sft-fix",
    #     "model_type": "eager",
    #     "prompt_template": "sft"
    # },
    "v3 241018-pretrain (eager)": {
        "model_name_or_repo_id": "p1atdev/dart-v3-llama-8L-241018-2",
        "model_type": "eager",
        "prompt_template": PROMPT_TEMPLATE_PRETRAIN,
    },
    "v3 241018+241020-use (eager)": {
        "model_name_or_repo_id": "p1atdev/dart-v3-llama-8L-241018_241020-sft-use",
        "model_type": "eager",
        "prompt_template": PROMPT_TEMPLATE_USE,
    },
    "v3 241005+241008-sft-fix (eager)": {
        "model_name_or_repo_id": "p1atdev/dart-v3-llama-8L-241005_241008-sft-fix",
        "model_type": "eager",
        "prompt_template": PROMPT_TEMPLATE_SFT,
    },
    "v3 241018+241020-use-group (eager)": {
        "model_name_or_repo_id": "p1atdev/dart-v3-llama-8L-241018_241020-sft-use-group",
        "revision": "12bdec918e8d1eea3e55b7950aff214745757620",
        "model_type": "eager",
        "prompt_template": PROMPT_TEMPLATE_USE,
    },
}

V3_FORM = {
    "rating": (
        V3_RATING_MAP.keys(),
        {
            "default": "general",
        },
    ),
    "length": (
        V3_LENGTH_MAP.keys(),
        {
            "default": "medium",
        },
    ),
    "aspect_ratio": (
        "STRING",
        {
            "default": "",
            "placeholder": "Aspect ratio tags (4:3, 16:9, ...)",
        },
    ),
}

V3_COPYRIGHT_TAGS_PATH = TAGS_ROOT_DIR / "v3" / "copyright.txt"
V3_CHARACTER_TAGS_PATH = TAGS_ROOT_DIR / "v3" / "character.txt"


def aspect_ratio_tag(
    width: int,
    height: int,
) -> str:
    """
    Returns aspect ratio tag based on the aspect ratio of the image.
    """
    ar = math.log2(width / height)

    if ar <= -1.25:
        return "too_tall"
    elif ar <= -0.75:
        return "tall_wallpaper"
    elif ar <= -0.25:
        return "tall"
    elif ar < 0.25:
        return "square"
    elif ar < 0.75:
        return "wide"
    elif ar < 1.25:
        return "wide_wallpaper"
    else:
        return "too_wide"


class V3Model(ModelWrapper):
    version = "v3"

    copyright_tags_path = V3_COPYRIGHT_TAGS_PATH
    character_tags_path = V3_CHARACTER_TAGS_PATH

    MODEL_TYPE = Literal["eager", "onnx"]

    model: MistralForCausalLM | ORTModelForCausalLM
    tokenizer: PreTrainedTokenizer | PreTrainedTokenizerBase

    prompt_template: str

    def __init__(
        self,
        model_name_or_repo_id: str,
        revision: str | None = None,
        model_type: MODEL_TYPE = "eager",
        onnx_file_name: str | None = None,
        prompt_template: str = PROMPT_TEMPLATE_SFT,
    ):
        if model_type == "eager":
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name_or_repo_id,
                revision=revision,
                torch_dtype=torch.bfloat16,
            )
            self.model.eval()
        elif model_type == "onnx":
            self.model = ORTModelForCausalLM.from_pretrained(
                model_name_or_repo_id,
                revision=revision,
                file_name=onnx_file_name,
                export=False,
            )
        else:
            raise ValueError(f"Invalid model type: {model_type}")
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name_or_repo_id, trust_remote_code=True
        )
        self.prompt_template = prompt_template

    def format_prompt(self, format_kwargs: dict[str, str]) -> str:
        return self.prompt_template.format(**format_kwargs)

    @torch.inference_mode()
    def generate(
        self,
        prompt: str,
        generation_config: GenerationConfig,
        **kwargs,
    ) -> tuple[str, str, str]:
        input_ids: torch.Tensor = self.tokenizer(prompt, return_tensors="pt").input_ids
        input_end_index = len(input_ids[0])

        output_ids = self.model.generate(
            input_ids, generation_config=generation_config
        )[0]  # take the first sequence
        output_full = self.decode_ids(output_ids)
        output_new = self.decode_ids(output_ids[input_end_index:])
        output_raw = self.decode_ids(output_ids, skip_special_tokens=False)

        return (output_full, output_new, output_raw)

    def decode_ids(
        self,
        generated_ids: torch.Tensor,  # (token_length,)
        skip_special_tokens: bool = True,
    ) -> str:
        # (token_length,) -> (token_length, 1)
        generated_ids = generated_ids.unsqueeze(1)

        return ", ".join(
            [
                token
                for token in self.tokenizer.batch_decode(
                    generated_ids, skip_special_tokens=skip_special_tokens
                )
                if token.strip() != ""
            ]
        )
