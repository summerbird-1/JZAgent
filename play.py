from Agent.agents.role_play import RolePlay


llm_config = {'model': 'qwen-max', 'model_server': 'dashscope'}
system_instruction = "你可以通过调用工具帮用户完成一些任务。对于模糊的问题不要瞎猜，先主动向用户询问具体细节以辅助完成任务。"
# function_list = ['binary_search', 'quick_sort', 'ask_human_for_help']
function_list = ['ask_human_for_help']

bot = RolePlay(llm=llm_config, instruction=system_instruction, function_list=function_list)
# bot = RolePlay(llm=llm_config, instruction=system_instruction)

response = bot.run("帮我对数组进行排序，然后给出4在排序后的数组中的位置", 
                   use_vs=True, 
                   vs_cfg={'storage_path': 'tool_vector_store', 'index_name': 'tool'}
                     )

text = ''
for chunk in response:
    text += chunk
