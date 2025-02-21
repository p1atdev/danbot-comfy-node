from transformers import GenerationConfig, set_seed


from ..models.utils import ModelWrapper
from ..models import v2408
from .type import (
    DANBOT_MODEL_TYPE,
    DANBOT_GENERATION_CONFIG_TYPE,
    DANBOT_CATEGORY,
    TEMPLATE_CONFIG_DTYPE,
)


INPUT_TYPES = {
    "required": {
        "danbot_model": (DANBOT_MODEL_TYPE,),
        "text_prompt": (
            "STRING",
            {
                "forceInput": True,
                "tooltip": "Natural language prompt. English and Japanese are supported.",
            },
        ),
        "seed": (
            "INT",
            {
                "default": 0,
                "step": 1,
                "min": 0,
                "max": 2**32 - 1,
                "display": "number",
            },
        ),
    },
    "optional": {
        "ban_tags": (
            "STRING",
            {
                "forceInput": True,
                "tooltip": "Tags to ban during generation",
            },
        ),
        "translation_template_config": (TEMPLATE_CONFIG_DTYPE,),
        "extension_template_config": (TEMPLATE_CONFIG_DTYPE,),
        "generation_config": (
            DANBOT_GENERATION_CONFIG_TYPE,
            {
                "tooltip": "Generation configuration for the upmsapling tags",
            },
        ),
    },
}


class V2408PipelineNode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return INPUT_TYPES

    RETURN_TYPES = (
        "STRING",
        "STRING",
        "STRING",
        "STRING",
    )
    RETURN_NAMES = (
        "generated_tags",
        "translated_tags",
        "extended_tags",
        "raw_output",
    )
    OUTPUT_TOOLIPS = (
        "The generated tags.",
        "The raw output of the model. This includes the special tokens.",
    )

    FUNCTION = "generate"

    OUTPUT_NODE = False

    CATEGORY = DANBOT_CATEGORY

    def generate(
        self,
        danbot_model: ModelWrapper,
        text_prompt: str,
        seed: int,
        ban_tags: str | None = None,
        translation_template_config: v2408.TemplateConfig = v2408.TemplateConfig(
            aspect_ratio="tall",
            rating="general",
            length="very_short",
        ),
        extension_template_config: v2408.TemplateConfig = v2408.TemplateConfig(
            aspect_ratio="tall",
            rating="general",
            length="long",
        ),
        generation_config: GenerationConfig = GenerationConfig(
            do_sample=False,
            max_new_tokens=256,
        ),
    ):
        set_seed(seed)
        # 1. translate
        translation_template = danbot_model.format_prompt(
            template_name="translation",
            format_kwargs={
                "aspect_ratio": v2408.ASPECT_RATIO_MAP[
                    translation_template_config.aspect_ratio
                ],
                "rating": v2408.RATING_MAP[translation_template_config.rating],
                "length": v2408.LENGTH_MAP[translation_template_config.length],
            },
        )
        _full, _new, raw = danbot_model.generate(
            text_prompt=text_prompt,
            tag_template=translation_template,
            generation_config=GenerationConfig(
                do_sample=False,
                max_new_tokens=generation_config.max_new_tokens,
            ),
            ban_tags=ban_tags,
            stop_token=v2408.TRANSLATION_END,
        )
        translation = danbot_model.extract_translation_result(raw)

        # 2. extend
        copyright_tags = translation.get("copyright", "")
        character_tags = translation.get("character", "")
        translation_tags = translation.get("translation", "")

        extension_template = danbot_model.format_prompt(
            template_name="extension",
            format_kwargs={
                "aspect_ratio": v2408.ASPECT_RATIO_MAP[
                    extension_template_config.aspect_ratio
                ],
                "rating": v2408.RATING_MAP[extension_template_config.rating],
                "length": v2408.LENGTH_MAP[extension_template_config.length],
                "copyright": copyright_tags,
                "character": character_tags,
                "translation": translation_tags,
            },
        )
        _full, _new, raw = danbot_model.generate(
            text_prompt=text_prompt,
            tag_template=extension_template,
            generation_config=generation_config,
            ban_tags=ban_tags,
            stop_token=v2408.EXTENSION_END,
        )
        extension = danbot_model.extract_extension_result(raw)

        extension_tags = extension.get("extension", "")
        output_tags = ", ".join(
            [
                part
                for part in (
                    copyright_tags,
                    character_tags,
                    translation_tags,
                    extension_tags,
                )
                if part.strip()
            ]
        )
        translated_tags = ", ".join(
            [
                part
                for part in (
                    copyright_tags,
                    character_tags,
                    translation_tags,
                )
                if part.strip()
            ]
        )

        return (
            output_tags,
            translated_tags,
            extension_tags,
            raw,
        )
