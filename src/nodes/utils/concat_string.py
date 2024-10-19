class ConcatStringNode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "string_former": ("STRING", {"forceInput": True}),
                "string_latter": ("STRING", {"forceInput": True}),
                "separator": ("STRING", {"default": ", "}),
            },
        }

    RETURN_TYPES = ("STRING",)

    FUNCTION = "concat"

    OUTPUT_NODE = False

    CATEGORY = "prompt/Danbooru Tags Transformer/utils"
    DESCRIPTION = "Concats the input strings."

    def concat(self, string_former: str, string_latter: str, separator: str = ", "):
        strings = [string_former, string_latter]
        result = separator.join(strings)
        return (result,)
