from .base import BaseTool, register_tool


@register_tool('finishing_success')
class FinishingSuccessTool(BaseTool):
    name = 'finishing_success'
    description = '在成功完成任务时调用此工具，并给出结果'
    parameters = [{
        'name': 'result',
        'description': '任务执行的结果',
        'required': True,
        'type': 'string'
    }]

    def call(self, params: str, **kwargs):
        params = self._verify_args(params)
        if isinstance(params, str):
            return "Parameter Error"
        
        return f"任务成功：{params['result']}"
