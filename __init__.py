from .src import nodes

NODE_CLASS_MAPPINGS = {
    "DanbotLoadModel": nodes.LoadModelNode,
    "DanbotGeneratorNode": nodes.GeneratorNode,
    "DanbotGenerationConfig": nodes.GenerationConfigNode,
    "DanbotTranslationExtractorNode": nodes.TranslationExtractorNode,
    "DanbotEtensionExtractorNode": nodes.ExtensionExtractorNode,
    "DanbotLoadBanTagsNode": nodes.LoadBanTagsNode,
    #
    "DanbotV2408AutoAspectRatioTag": nodes.V2408AutoAspectRatioTagNode,
    "DanbotV2408PipelineNode": nodes.V2408PipelineNode,
    #
    "DanbotV2408TemplateConfigNode": nodes.V2408TemplateConfigNode,
    "DanbotV2408FormatterNode": nodes.V2408FormatterNode,
    #
    "DanbotUtilsPrintString": nodes.PrintStringNode,
    "DanbotUtilsConcatString": nodes.ConcatStringNode,
    "DanbotUtilsTextInput": nodes.TextInputNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DanbotLoadModel": "Danbot Load Model",
    "DanbotGeneratorNode": "Danbot Generator",
    "DanbotGenerationConfig": "Danbot Generation Config",
    "DanbotTranslationExtractorNode": "Danbot Translation Extractor",
    "DanbotEtensionExtractorNode": "Danbot Extension Extractor",
    "DanbotLoadBanTagsNode": "Danbot Load Ban Tags",
    #
    "DanbotV2408AutoAspectRatioTag": "Danbot V2408 Auto Aspect Ratio Tag",
    "DanbotV2408PipelineNode": "Danbot V2408 Pipeline",
    #
    "DanbotV2408TemplateConfigNode": "Danbot V2408 Template Config",
    "DanbotV2408FormatterNode": "Danbot V2408 Formatter",
    #
    "DanbotUtilsPrintString": "Danbot Print String",
    "DanbotUtilsConcatString": "Danbot Concat String",
    "DanbotUtilsEscapeBrackets": "Danbot Escape Brackets",
    "DanbotUtilsTextInput": "Danbot Text Input",
}

WEB_DIRECTORY = "./src/js"
