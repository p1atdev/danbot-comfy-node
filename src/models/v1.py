from typing import Literal
import logging

import torch

from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    OPTForCausalLM,
    PreTrainedTokenizerBase,
    GenerationConfig,
)
from optimum.onnxruntime.modeling_decoder import ORTModelForCausalLM

from .utils import (
    ModelWrapper,
)
from ..tags import TAGS_ROOT_DIR

V1_RATING_MAP = {
    "general": "rating:sfw, rating:general",
    "sensitive": "rating:sfw, rating:sensitive",
    "questionable": "rating:nsfw, rating:questionable",
    "explicit": "rating:nsfw, rating:explicit",
}

V1_LENGTH_MAP = {
    "very_short": "<|very_short|>",
    "short": "<|short|>",
    "long": "<|long|>",
    "very_long": "<|very_long|>",
}


PROMPT_TEMPLATE_SFT = (
    "<|bos|>"
    "<rating>{rating}</rating>"
    "<copyright>{copyright}</copyright>"
    "<character>{character}</character>"
    "{length}"
    "<general>{condition}<|input_end|>"
).strip()

V1_MODELS = {
    "v1 sft (eager)": {
        "model_name_or_repo_id": "p1atdev/dart-v1-sft",
        "model_type": "eager",
        "prompt_template": PROMPT_TEMPLATE_SFT,
    },
    "v1 sft (onnx)": {
        "model_name_or_repo_id": "p1atdev/dart-v1-sft",
        "model_type": "onnx",
        "onnx_file_name": "model.onnx",
        "prompt_template": PROMPT_TEMPLATE_SFT,
    },
    "v1 sft (onnx quant)": {
        "model_name_or_repo_id": "p1atdev/dart-v1-sft",
        "model_type": "onnx",
        "onnx_file_name": "model_quantized.onnx",
        "prompt_template": PROMPT_TEMPLATE_SFT,
    },
}

V1_COPYRIGHT_TAGS_PATH = TAGS_ROOT_DIR / "v1" / "copyright.txt"
V1_CHARACTER_TAGS_PATH = TAGS_ROOT_DIR / "v1" / "character.txt"


class V1Model(ModelWrapper):
    version = "v1"

    copyright_tags_path = V1_COPYRIGHT_TAGS_PATH
    character_tags_path = V1_CHARACTER_TAGS_PATH

    MODEL_TYPE = Literal["eager", "onnx"]

    model: OPTForCausalLM | ORTModelForCausalLM
    tokenizer: PreTrainedTokenizerBase

    prompt_template: str = PROMPT_TEMPLATE_SFT

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
        negative_prompt: str | None = None,
        ban_tags: str | None = None,
        **kwargs,
    ) -> tuple[str, str, str]:
        input_ids = self.tokenizer(prompt, return_tensors="pt").input_ids

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
            ban_token_ids=ban_token_ids,
        )[0]  # take the first sequence
        output_full = self.decode_ids(output_ids)
        output_new = self.decode_ids(output_ids[len(input_ids[0]) :])
        output_raw = self.decode_ids(output_ids)

        return (output_full, output_new, output_raw)

    def decode_ids(
        self,
        generated_ids: torch.Tensor,
    ) -> str:
        return self.tokenizer.decode(generated_ids, skip_special_tokens=True)
