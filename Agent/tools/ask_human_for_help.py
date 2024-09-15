from .base import BaseTool, register_tool


@register_tool('ask_human_for_help')
class AskHumanForHelpTool(BaseTool):
    name = 'ask_human_for_help'
    description = """用户求助工具，如果你对于要解决的任务有任何不清楚的地方，可以用这个工具向用户询问相关信息。
    例如：用户问你今天天气如何，但是你不知道该用户所在的地理位置，你可以使用这个工具向用户询问地理位置。"""
    parameters = [{
        'name': 'question',
        'description': '向用户提问你需要获取的信息',
        'required': True,
        'type': 'string'
    }]

    def call(self, params: str, **kwargs) -> str:
        params = self._verify_args(params)
        if isinstance(params, str):
            return "Parameter Error"
        
        question = params['question']
        human_answer = input(question + '\n')
        return human_answer
