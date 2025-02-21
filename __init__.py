from .src import nodes

NODE_CLASS_MAPPINGS = {
    "DanbotLoadModel": nodes.LoadModelNode,
    "DanbotUpsamplerNode": nodes.UpsamplerNode,
    "DanbotTranslatorNode": nodes.TranslatorNode,
    "DanbotExtenderNode": nodes.ExtenderNode,
    "DanbotGenerationConfig": nodes.GenerationConfigNode,
    "DanbotLoadBanTagsNode": nodes.LoadBanTagsNode,
    #
    "DanbotV2408AutoAspectRatioTag": nodes.V2408AutoAspectRatioTagNode,
    #
    "DanbotV2408FormatterNode": nodes.V2408FormatterNode,
    #
    "DanbotUtilsPrintString": nodes.PrintStringNode,
    "DanbotUtilsConcatString": nodes.ConcatStringNode,
    "DanbotUtilsTextInput": nodes.TextInputNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DanbotLoadModel": "Danbot Load Model",
    "DanbotUpsamplerNode": "Danbot Upsampler",
    "DanbotTranslatorNode": "Danbot Translator",
    "DanbotExtenderNode": "Danbot Extender",
    "DanbotGenerationConfig": "Danbot Generation Config",
    "DanbotLoadBanTagsNode": "Danbot Load Ban Tags",
    #
    "DanbotV2408AutoAspectRatioTag": "Danbot V2408 Auto Aspect Ratio Tag",
    #
    "DanbotV2408FormatterNode": "Danbot V2408 Formatter",
    #
    "DanbotUtilsPrintString": "Danbot Print String",
    "DanbotUtilsConcatString": "Danbot Concat String",
    "DanbotUtilsEscapeBrackets": "Danbot Escape Brackets",
    "DanbotUtilsTextInput": "Danbot Text Input",
}

WEB_DIRECTORY = "./src/js"
