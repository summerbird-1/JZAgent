from Agent.tools.base import BaseTool, register_tool
import json5


def quick_sort(arr) -> list[int]:
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

@register_tool('quick_sort')
class QuickSortTool(BaseTool):
    name = 'quick_sort'
    description = '快速排序工具，输入一个数组，返回排序后的数组。'
    parameters = [{
        'name': 'arr',
        'description': '待排序的数组',
        'required': True,
        'type': 'array'
    }]

    def call(self, params: str, **kwargs) -> str:
        params = self._verify_args(params)
        if isinstance(params, str):
            return "Parameter Error"

        return str(quick_sort(json5.loads(params['arr'])))
