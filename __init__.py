from .src import nodes

NODE_CLASS_MAPPINGS = {
    "DartUpsamplerNode": nodes.UpsamplerNode,
    "DartLoadModel": nodes.LoadModelNode,
    "DartV2AutoAspectRatioTag": nodes.V2AutoAspectRatioTagNode,
    "DartV3AutoAspectRatioTag": nodes.V3AutoAspectRatioTagNode,
    "DartGenerationConfig": nodes.GenerationConfigNode,
    "DartV2FormatterNode": nodes.V2FormatterNode,
    "DartV3FormatterNode": nodes.V3FormatterNode,
    "DartUtilsPrintString": nodes.PrintStringNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DartUpsamplerNode": "Dart Upsampler Node",
    "DartLoadModel": "Dart Load Model",
    "DartV2AutoAspectRatioTag": "Dart V2 Auto Aspect Ratio Tag",
    "DartV3AutoAspectRatioTag": "Dart V3 Auto Aspect Ratio Tag",
    "DartGenerationConfig": "Dart Generation Config",
    "DartV2FormatterNode": "Dart V2 Formatter Node",
    "DartV3FormatterNode": "Dart V3 Formatter Node",
    "DartUtilsPrintString": "Dart Print String",
}

WEB_DIRECTORY = "./src/js"
