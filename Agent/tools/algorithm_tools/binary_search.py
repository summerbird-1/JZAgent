from Agent.tools.base import BaseTool, register_tool
import json5


def binary_search(arr, target):
    low = 0
    high = len(arr) - 1

    while low <= high:
        mid = (low + high) // 2

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    return -1

@register_tool('binary_search')
class BinarySearchTool(BaseTool):
    name = 'binary_search'
    description = '二分查找工具，输入一个有序数组和目标值，返回目标值在数组中的索引。若不存在则返回-1。'
    parameters = [{
        'name': 'arr',
        'description': '有序数组',
        'required': True,
        'type': 'array'
    }, {
        'name': 'target',
        'description': '待查找的目标值',
        'required': True,
        'type': 'number'
    }]

    def call(self, params: str, **kwargs) -> int:
        params = self._verify_args(params)
        if isinstance(params, str):
            return "Parameter Error"
        
        arr = json5.loads(params['arr'])
        target = json5.loads(params['target'])

        return str(binary_search(arr, target))
