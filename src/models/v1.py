from typing import Literal

from .utils import ModelWrapper

import torch

from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    OPTForCausalLM,
    PreTrainedTokenizerBase,
    PreTrainedModel,
    BatchEncoding,
    GenerationConfig,
)
from optimum.onnxruntime.modeling_decoder import ORTModelForCausalLM

V1_MODELS = {
    "v1 (eager)": {
        "model": "p1atdev/dart-v1-sft",
        "model_type": "eager",
    },
    "v1 (onnx)": {
        "model": "p1atdev/dart-v1-sft",
        "model_type": "onnx",
        "onnx_model_file": "model.onnx",
    },
    "v1 (quantized onnx)": {
        "model": "p1atdev/dart-v1-sft",
        "model_type": "onnx",
        "onnx_model_file": "model_quantized.onnx",
    },
}

V1_FORMAT_CHOICES = {
    "rating": ["general", "sensitive", "questionable", "explicit"],
    "length": ["very_short", "short", "long", "very_long"],
}
V1_FORM = {
    "copyright": (
        "STRING",
        {
            "default": "",
            "placeholder": "Copyright tags (vocaloid, ...)",
        },
    ),
    "character": (
        "STRING",
        {
            "default": "",
            "placeholder": "Character tags (hatsune miku, ...)",
        },
    ),
    "general": (
        "STRING",
        {
            "default": "",
            "placeholder": "General tags (1girl, solo, ...)",
        },
    ),
}


class V1Model(ModelWrapper):
    MODEL_TYPE = Literal["eager", "onnx"]

    model: OPTForCausalLM | ORTModelForCausalLM
    tokenizer: PreTrainedTokenizerBase

    def __init__(
        self,
        model_name_or_repo_id: str,
        model_type: MODEL_TYPE = "eager",
        onnx_file_name: str | None = None,
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

    def compose_prompt(self, format_kwargs: dict[str, str]) -> BatchEncoding:
        encoded: BatchEncoding = self.tokenizer.apply_chat_template(
            format_kwargs,  # type: ignore
            return_tensors="pt",
            tokenize=True,
        )
        return encoded

    @torch.inference_mode()
    def generate(
        self, input_ids: torch.Tensor, generation_config: GenerationConfig
    ) -> torch.LongTensor:
        outputs = self.model.generate(input_ids, generation_config=generation_config)
        return outputs

    def decode_ids(
        self,
        generated_ids: torch.LongTensor,
    ) -> str:
        return self.tokenizer.decode(generated_ids, skip_special_tokens=True)
