from typing import Literal
import math

import torch

from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    MistralForCausalLM,
    PreTrainedTokenizerBase,
    GenerationConfig,
)
from optimum.onnxruntime.modeling_decoder import ORTModelForCausalLM

from .utils import (
    ModelWrapper,
)
from ..tags import TAGS_ROOT_DIR


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
        model_name_or_path: str,
        prompt_template: str,
        model_type: MODEL_TYPE = "eager",
        onnx_file_name: str | None = None,
    ):
        if model_type == "eager":
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name_or_path,
                torch_dtype=torch.bfloat16,
            )
            self.model.eval()
        elif model_type == "onnx":
            self.model = ORTModelForCausalLM.from_pretrained(
                model_name_or_path,
                file_name=onnx_file_name,
                export=False,
            )
        else:
            raise ValueError(f"Invalid model type: {model_type}")
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name_or_path, trust_remote_code=True
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
            bad_words_ids=ban_token_ids,
        )[0]  # take the first sequence
        output_full = self.decode_ids(output_ids)
        output_new = self.decode_ids(output_ids[len(input_ids[0]) :])
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
