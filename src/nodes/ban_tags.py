from typing import Literal
import os
from pathlib import Path

from ..tags import TAGS_ROOT_DIR, load_tags, normalize_tag_text

BAN_TEMPLATE_DIR = TAGS_ROOT_DIR / "ban_template"


def list_ban_template_files(dir: Path):
    files = os.listdir(BAN_TEMPLATE_DIR)
    files = [file for file in files if file.endswith(".txt")]

    return files


def load_ban_template(file: str):
    return load_tags(BAN_TEMPLATE_DIR / file)


class LoadBanTagsNode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        files = list_ban_template_files(BAN_TEMPLATE_DIR)

        return {
            "optional": {
                "template_name": (files,),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("ban_tags",)
    OUTPUT_TOOLTIPS = ("Comma separated tags to ban",)

    FUNCTION = "compose"

    OUTPUT_NODE = False

    CATEGORY = "prompt/Danbooru Tags Transformer"

    def compose(
        self,
        template: str | None,
    ):
        tags = load_ban_template(template) if template else []

        tag_text = normalize_tag_text(",".join(tags))

        return (tag_text,)
