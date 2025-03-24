from dataclasses import dataclass
from typing import Any, Literal
from abc import ABC
import math
import re

import torch

from transformers import (
    AutoModelForPreTraining,
    AutoProcessor,
    GenerationConfig,
    PreTrainedModel,
    BatchFeature,
)

from .utils import (
    ModelWrapper,
    EncoderDecoderTokenizer,
    AbstractTemplateConfig,
    is_flash_attn_available,
)

RATING_MAP = {
    "general": "<|rating:general|>",
    "sensitive": "<|rating:sensitive|>",
    "questionable": "<|rating:questionable|>",
    "explicit": "<|rating:explicit|>",
}

LENGTH_MAP = {
    "very_short": "<|length:very_short|>",
    "short": "<|length:short|>",
    "long": "<|length:long|>",
    "very_long": "<|length:very_long|>",
}

ASPECT_RATIO_MAP = {
    "too_tall": "<|aspect_ratio:too_tall|>",
    "tall_wallpaper": "<|aspect_ratio:tall_wallpaper|>",
    "tall": "<|aspect_ratio:tall|>",
    "square": "<|aspect_ratio:square|>",
    "wide": "<|aspect_ratio:wide|>",
    "wide_wallpaper": "<|aspect_ratio:wide_wallpaper|>",
    "too_wide": "<|aspect_ratio:too_wide|>",
}

INPUT_END = "<|input_end|>"
TRANSLATION_END = "<|reserved_6|>"
EXTENSION_END = "</general>"

COPYRIGHT_TAGS_PATTERN = re.compile(r"<copyright>(.*?)</copyright>")
CHARACTER_TAGS_PATTERN = re.compile(r"<character>(.*?)</character>")
TRANSLATION_TAGS_PATTERN = re.compile(r"<translation>(.*?)</translation>")
EXTENSION_TAGS_PATTERN = re.compile(r"<extension>(.*?)</extension>")

TEMPLATE_NAME = Literal["translation", "extension"]
TEMPLATE_NAMES = ["translation", "extension"]


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


@dataclass
class TemplateConfig(AbstractTemplateConfig):
    aspect_ratio: str
    rating: str
    length: str


class V2408Processor(EncoderDecoderTokenizer, ABC):
    def __call__(self, encoder_text: str, decoder_text: str, **kwargs) -> Any:
        pass


class _Model(PreTrainedModel, ABC):
    encoder_model: PreTrainedModel
    decoder_model: PreTrainedModel


class V2408Model(ModelWrapper):
    version = "v2408"

    copyright_tags_pattern = COPYRIGHT_TAGS_PATTERN
    character_tags_pattern = CHARACTER_TAGS_PATTERN

    model: _Model
    processor: V2408Processor

    prompt_templates: dict[TEMPLATE_NAME, str]
    prompt_templates_default: dict[TEMPLATE_NAME, dict[str, str]] = {
        "translation": {},
        "extension": {
            "copyright": "",
            "character": "",
            "translation": "",
        },
    }

    def __init__(
        self,
        model_name_or_path: str,
        prompt_templates: dict[TEMPLATE_NAME, str],
        revision: str | None = None,
        trust_remote_code: bool = False,
    ):
        load_device = self._get_device()

        self.model = AutoModelForPreTraining.from_pretrained(
            model_name_or_path,
            revision=revision,
            torch_dtype=torch.bfloat16,
            trust_remote_code=trust_remote_code,
            attn_implementation=(
                "flash_attention_2"
                if (is_flash_attn_available() and load_device.type == "cuda")
                else "sdpa"
            ),
        )
        self.model.to(load_device)  # type: ignore
        self.model.eval()
        self.processor = AutoProcessor.from_pretrained(
            model_name_or_path,
            revision=revision,
            trust_remote_code=trust_remote_code,
        )
        self.prompt_templates = prompt_templates

    def format_prompt(self, template_name: str, format_kwargs: dict[str, str]) -> str:
        assert template_name in self.prompt_templates, (
            f'Template name "{template_name}" not found.'
        )
        return self.prompt_templates[template_name].format(**format_kwargs)

    @torch.inference_mode()
    def generate(
        self,
        text_prompt: str,
        tag_template: str,
        generation_config: GenerationConfig,
        ban_tags: str | None = None,
        stop_token: str | None = None,
        **kwargs,
    ) -> tuple[str, str, str]:
        inputs: BatchFeature = self.processor(
            encoder_text=text_prompt,
            decoder_text=tag_template,
            return_tensors="pt",
        ).to(self.model.device)
        input_ids_len = len(inputs.input_ids[0])

        ban_token_ids = None
        if ban_tags is not None:
            ban_token_ids = self.encode_ban_tags(ban_tags)

        stop_token_id = self.processor.decoder_tokenizer.eos_token_id
        if stop_token is not None:
            stop_token_id = self.processor.decoder_tokenizer(
                stop_token, return_tensors="pt"
            ).input_ids

        output_ids = self.model.generate(
            **inputs,
            generation_config=generation_config,
            bad_words_ids=ban_token_ids,
            eos_token_id=stop_token_id,
            pad_token_id=self.processor.decoder_tokenizer.pad_token_id,
        )[0]  # take the first sequence
        output_full = self.decode_ids(output_ids)
        output_completion = self.decode_ids(output_ids[input_ids_len:])
        output_raw = self.decode_ids(output_ids, skip_special_tokens=False)

        return (output_full, output_completion, output_raw)

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
                for token in self.processor.decoder_tokenizer.batch_decode(
                    generated_ids, skip_special_tokens=skip_special_tokens
                )
                if token.strip() != ""
            ]
        )

    def extract_translation_result(self, raw_output: str) -> dict[str, str]:
        copyright_tags = self.search_tags(raw_output, self.copyright_tags_pattern)
        character_tags = self.search_tags(raw_output, self.character_tags_pattern)
        translation_tags = self.search_tags(raw_output, TRANSLATION_TAGS_PATTERN)

        return {
            "copyright": copyright_tags,
            "character": character_tags,
            "translation": translation_tags,
        }

    def extract_extension_result(self, raw_output: str) -> dict[str, str]:
        extension_tags = self.search_tags(raw_output, EXTENSION_TAGS_PATTERN)

        return {"extension": extension_tags}
