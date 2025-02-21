from ..type import DANBOT_CATEGORY


class TextInputNode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "optional": {
                "text": (
                    "STRING",
                    {
                        "multiline": True,
                    },
                ),
            },
        }

    RETURN_TYPES = ("STRING",)

    FUNCTION = "passthrough"

    CATEGORY = DANBOT_CATEGORY + "/utils"
    DESCRIPTION = (
        "Just pass the given text to the next nodes without any transformation."
    )

    def passthrough(self, text=None):
        if text is not None:
            return (text,)
        return ()
