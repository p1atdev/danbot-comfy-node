def escape_important(text):
    text = text.replace("(", "\\(")
    text = text.replace(")", "\\)")
    return text


class EscapeBracketsNode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {"forceInput": True}),
            },
        }

    RETURN_TYPES = ("STRING",)

    FUNCTION = "escape"

    OUTPUT_NODE = False

    CATEGORY = "prompt/Danbooru Tags Transformer/utils"
    DESCRIPTION = "Concats the input strings."

    def escape(self, text: str):
        return (escape_important(text),)
