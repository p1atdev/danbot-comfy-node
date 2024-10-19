from .src import (
    UpsamplerNode,
    LoadModelNode,
    AutoAspectRatioTagNode,
    PrintStringNode,
    GenerationConfigNode,
    V3FormatterNode,
)

NODE_CLASS_MAPPINGS = {
    "DartUpsamplerNode": UpsamplerNode,
    "DartLoadModel": LoadModelNode,
    "DartAutoAspectRatioTag": AutoAspectRatioTagNode,
    "DartGenerationConfig": GenerationConfigNode,
    "DartV3FormatterNode": V3FormatterNode,
    "DartUtilsPrintString": PrintStringNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DartUpsamplerNode": "Dart Upsampler Node",
    "DartLoadModel": "Dart Load Model",
    "DartAutoAspectRatioTag": "Dart Auto Aspect Ratio Tag",
    "DartGenerationConfig": "Dart Generation Config",
    "DartV3FormatterNode": "Dart V3 Formatter Node",
    "DartUtilsPrintString": "Dart Print String",
}

WEB_DIRECTORY = "./src/js"
