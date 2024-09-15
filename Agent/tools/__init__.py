from .base import TOOL_REGISTRY, BaseTool, register_tool

from .algorithm_tools.binary_search import BinarySearchTool
from .algorithm_tools.quick_sort import QuickSortTool

from .ask_human_for_help import AskHumanForHelpTool

from .finishing_failure import FinishingFailureTool
from .finishing_success import FinishingSuccessTool


from .dashscope_tools.image_generator import TextToImageTool


# def call_tool(plugin_name: str, plugin_args: str) -> str:
#     if plugin_name in TOOL_REGISTRY:
#         return TOOL_REGISTRY[plugin_name].call(plugin_args)
#     else:
#         raise NotImplementedError


__all__ = ['BaseTool', 'TOOL_REGISTRY', 'register_tool']
