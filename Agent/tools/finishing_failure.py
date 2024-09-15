from .base import BaseTool, register_tool


@register_tool('finishing_failure')
class FinishingFailureTool(BaseTool):
    name = 'finishing_failure'
    description = "如果你在执行任务时遇到了无法解决的问题，可以使用这个工具放弃执行，并且告知用户原因。"
    parameters = [{
        'name': 'reason',
        'description': '放弃执行的原因',
        'required': True,
        'type': 'string'
    }]

    def call(self, params: str, **kwargs) -> str:
        params = self._verify_args(params)
        if isinstance(params, str):
            return "Parameter Error"
        
        return f"任务失败：{params['reason']}"
