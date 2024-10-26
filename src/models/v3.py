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
)
from ..tags import TAGS_ROOT_DIR

V3_RATING_MAP = {
    "general": "<|rating:general|>",
    "sensitive": "<|rating:sensitive|>",
    "questionable": "<|rating:questionable|>",
    "explicit": "<|rating:explicit|>",
}

V3_LENGTH_MAP = {
    "very_short": "<|length:very_short|>",
    # "short": "<|length:short|>",
    "medium": "<|length:medium|>",
    # "long": "<|length:long|>",
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
    "v3 sft 241018+241020-use-group": {
        "model_name_or_repo_id": "p1atdev/dart-v3-sft-test-241018_241020-UG",
        "model_type": "eager",
        "prompt_template": PROMPT_TEMPLATE_USE,
    },
    "v3 sft 241018+241022": {
        "model_name_or_repo_id": "p1atdev/dart-v3-llama-8L-241018_241022-sft",
        "model_type": "eager",
        "prompt_template": PROMPT_TEMPLATE_SFT,
    },
    "v3 sft 241018+241023": {
        "model_name_or_repo_id": "p1atdev/dart-v3-llama-8L-241018_241023-sft-1",
        "model_type": "eager",
        "prompt_template": PROMPT_TEMPLATE_SFT,
    },
    "v3 sft 241018+241023 2": {
        "model_name_or_repo_id": "p1atdev/dart-v3-llama-8L-241018_241023-sft-2",
        "model_type": "eager",
        "prompt_template": PROMPT_TEMPLATE_SFT,
    },
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
        negative_prompt: str | None = None,
        ban_tags: str | None = None,
        **kwargs,
    ) -> tuple[str, str, str]:
        input_ids: torch.Tensor = self.tokenizer(prompt, return_tensors="pt").input_ids
        input_end_index = len(input_ids[0])

        negative_input_ids = None
        if negative_prompt is not None:
            negative_input_ids = self.tokenizer(
                negative_prompt, return_tensors="pt"
            ).input_ids

        ban_token_ids = None
        if ban_tags is not None:
            ban_token_ids = self.encode_ban_tags(ban_tags)

        output_ids = self.model.generate(
            input_ids,
            generation_config=generation_config,
            negative_prompt_ids=negative_input_ids,
            bad_words_ids=ban_token_ids,
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
