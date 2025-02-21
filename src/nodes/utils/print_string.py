from ..type import DANBOT_CATEGORY


class PrintStringNode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "optional": {
                "input_string": ("STRING", {"forceInput": True}),
            },
        }

    RETURN_TYPES = ("STRING",)

    FUNCTION = "print_string"

    OUTPUT_NODE = True

    CATEGORY = DANBOT_CATEGORY + "/utils"
    DESCRIPTION = "Prints the input string to the console."

    def print_string(self, input_string=None):
        if input_string is not None:
            print("input_string:", input_string)
            return {
                "ui": {"text": (input_string,)},  # pass to JS message
                "result": (input_string,),
            }
        return ()
