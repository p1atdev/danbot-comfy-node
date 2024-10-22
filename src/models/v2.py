from typing import Literal
import math

import torch

from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    MistralForCausalLM,
    PreTrainedTokenizerBase,
    PreTrainedModel,
    BatchEncoding,
    GenerationConfig,
)
from optimum.onnxruntime.modeling_decoder import ORTModelForCausalLM

from .utils import (
    ModelWrapper,
    TAGS_ROOT_DIR,
)

V2_RATING_MAP = {
    "sfw": "<|rating:sfw|>",
    "general": "<|rating:general|>",
    "sensitive": "<|rating:sensitive|>",
    "nsfw": "<|rating:nsfw|>",
    "questionable": "<|rating:questionable|>",
    "explicit": "<|rating:explicit|>",
}

V2_LENGTH_MAP = {
    "very_short": "<|length:very_short|>",
    "short": "<|length:short|>",
    "medium": "<|length:medium|>",
    "long": "<|length:long|>",
    "very_long": "<|length:very_long|>",
}

V2_ASPECT_RATIO_MAP = {
    "ultra_tall": "<|aspect_ratio:ultra_tall|>",
    "very_tall": "<|aspect_ratio:very_tall|>",
    "tall": "<|aspect_ratio:tall|>",
    "square": "<|aspect_ratio:square|>",
    "wide": "<|aspect_ratio:wide|>",
    "very_wide": "<|aspect_ratio:very_wide|>",
    "ultra_wide": "<|aspect_ratio:ultra_wide|>",
}

V2_IDENTITY_MAP = {
    "none": "<|identity:none|>",
    "lax": "<|identity:lax|>",
    "strict": "<|identity:strict|>",
}


PROMPT_TEMPLATE_SFT = (
    "<|bos|>"
    "<copyright>{copyright}</copyright>"
    "<character>{character}</character>"
    "{rating}{aspect_ratio}{length}"
    "<general>{condition}{identity}<|input_end|>"
).strip()

V2_MODELS = {
    "v2 sft (eager)": {
        "model_name_or_repo_id": "p1atdev/dart-v2-sft",
        "model_type": "eager",
        "prompt_template": PROMPT_TEMPLATE_SFT,
    },
    "v2 sft (onnx quantized)": {
        "model_name_or_repo_id": "p1atdev/dart-v2-sft",
        "model_type": "onnx",
        "onnx_file_name": "model_quantized.onnx",
        "prompt_template": PROMPT_TEMPLATE_SFT,
    },
    "v2 MoE sft (eager)": {
        "model_name_or_repo_id": "p1atdev/dart-v2-moe-sft",
        "model_type": "eager",
        "prompt_template": PROMPT_TEMPLATE_SFT,
    },
}

V2_COPYRIGHT_TAGS_PATH = TAGS_ROOT_DIR / "v2" / "copyright.txt"
V2_CHARACTER_TAGS_PATH = TAGS_ROOT_DIR / "v2" / "character.txt"


def aspect_ratio_tag(
    width: int,
    height: int,
) -> str:
    """
    Returns aspect ratio tag based on the aspect ratio of the image.
    """
    ar = width / height

    if ar <= 1 / 2:
        return "too_tall"
    elif ar <= 8 / 9:
        return "tall"
    elif ar < 9 / 8:
        return "square"
    elif ar < 2:
        return "wide"
    else:
        return "too_wide"


class V2Model(ModelWrapper):
    version = "v2"

    copyright_tags_path = V2_COPYRIGHT_TAGS_PATH
    character_tags_path = V2_CHARACTER_TAGS_PATH

    MODEL_TYPE = Literal["eager", "onnx"]

    model: MistralForCausalLM | ORTModelForCausalLM
    tokenizer: PreTrainedTokenizerBase

    prompt_template: str

    def __init__(
        self,
        model_name_or_repo_id: str,
        model_type: MODEL_TYPE = "eager",
        onnx_file_name: str | None = None,
        prompt_template: str = PROMPT_TEMPLATE_SFT,
    ):
        if model_type == "eager":
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name_or_repo_id,
                torch_dtype=torch.bfloat16,
            )
            self.model.eval()
        elif model_type == "onnx":
            self.model = ORTModelForCausalLM.from_pretrained(
                model_name_or_repo_id,
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
        input_ids = self.tokenizer(prompt, return_tensors="pt").input_ids
        output_ids = self.model.generate(
            input_ids, generation_config=generation_config
        )[0]  # take the first sequence
        output_full = self.decode_ids(output_ids)
        output_new = output_full[len(input_ids[0]) :]
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
