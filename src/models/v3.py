from typing import Literal
import math

import torch

from .utils import ModelWrapper


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

PROMPT_TEMPLATE_PRETRAIN = (
    "<|bos|>"
    "{rating}{aspect_ratio}{length}"
    "<copyright>{copyright}</copyright>"
    "<character>{character}</character>"
    "<general>{condition}"
).strip()

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
        elif model_type == "onnx":
            self.model = ORTModelForCausalLM.from_pretrained(
                model_name_or_repo_id,
                file_name=onnx_file_name,
                export=False,
            )
        else:
            raise ValueError(f"Invalid model type: {model_type}")
        self.model.eval()
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
    ) -> torch.LongTensor:
        input_ids = self.tokenizer(prompt, return_tensors="pt").input_ids
        output_ids = self.model.generate(
            input_ids, generation_config=generation_config
        )[0]  # take the first sequence
        output = self.decode_ids(output_ids)

        return output

    def decode_ids(
        self,
        generated_ids: torch.Tensor,  # (token_length,)
    ) -> str:
        # (token_length,) -> (token_length, 1)
        generated_ids = generated_ids.unsqueeze(1)

        return ", ".join(
            [
                token
                for token in self.tokenizer.batch_decode(
                    generated_ids, skip_special_tokens=True
                )
                if token.strip() != ""
            ]
        )
