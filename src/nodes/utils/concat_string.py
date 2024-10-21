class ConcatStringNode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "optional": {
                "string_1": ("STRING", {"forceInput": True}),
                "string_2": ("STRING", {"forceInput": True}),
                "string_3": ("STRING", {"forceInput": True}),
                "string_4": ("STRING", {"forceInput": True}),
                "string_5": ("STRING", {"forceInput": True}),
                "string_6": ("STRING", {"forceInput": True}),
                "separator": ("STRING", {"default": ", "}),
            },
        }

    RETURN_TYPES = ("STRING",)

    FUNCTION = "concat"

    OUTPUT_NODE = False

    CATEGORY = "prompt/Danbooru Tags Transformer/utils"
    DESCRIPTION = "Concats the input strings."

    def concat(
        self,
        string_1: str = "",
        string_2: str = "",
        string_3: str = "",
        string_4: str = "",
        string_5: str = "",
        string_6: str = "",
        separator: str = ", ",
    ):
        strings = [string_1, string_2, string_3, string_4, string_5, string_6]
        strings = [string.strip() for string in strings if string.strip()]
        result = separator.join(strings)
        return (result,)
