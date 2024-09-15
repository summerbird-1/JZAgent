# ZXAgent

An simple agent framework based on [modelscope-agent](https://github.com/modelscope/modelscope-agent) and made some improvement on it. Some inspiration also comes from [XAgent](https://github.com/OpenBMB/XAgent). This project is just for learning.

## Some Improvement

1. Adjust the code structure. The output format of the model will only differ depending on the model interface, so the _detect_tool() method can be removed from the Agent base class and its subclass objects and added to the llm base class and its subclass. In this way, the framework maintainer overrides the _detect_tool method of the llm subclass when extending the model type (a necessary work), and the framework user no longer needs to worry about how to parse it when building his own Agent subclass object. For model output, you can directly call the _detect_tool() method of the llm object maintained by the Agent object, which unifies the interface and reduces redundancy.
2. Integrate the function_retrieve function into the Agent base class, and users can start the construction and loading of function_retriever on demand. Agent subclasses do not need to care about the specific implementation and execution process of function_retriever. The Agent base class will update the searched functions into function_map, which is compatible with directly specifying function_list.
3. Copy and paste the more robust tool detection logic in alpha_umi of modelscope-agent into the _detect_tool() method that has been adjusted to the llm base class. Agent objects can use this more robust tool detection method directly through the llm object they maintain.
4. Implement a simple ask_human_for_help tool.

## Components

1. **LLMs** which are able to generate function callings given instruction and function_list.
2. **Function repository**. Each function has description, name and parameters.
3. **Tool retriever** that can retieve needed functions from function repository given instruction. Implemented by an embedding model.
4. **Agent** which is activated by prompt, LLMs and function_list.

## An Example

First tell the agent explicitly that there is a tool called ask_human_for_help. Then, invoke "run()" method with arguments use_vs and vs_cfg (vs means vector store) so that the agent can retrieve needed function given my request. **Note** that the user_request I give the agent don't specify what array I want to sort. Instead of yielding hallucination, the agent ask me for more detailed information to complete the task then.

```python
from Agent.agents.role_play import RolePlay


llm_config = {'model': 'qwen-max', 'model_server': 'dashscope'}
system_instruction = "你可以通过调用工具帮用户完成一些任务。对于模糊的问题不要瞎猜，先主动向用户询问具体细节以辅助完成任务。"
function_list = ['ask_human_for_help']

bot = RolePlay(llm=llm_config, instruction=system_instruction, function_list=function_list)

response = bot.run("帮我对数组进行排序，然后给出4在排序后的数组中的位置", 
                   use_vs=True, 
                   vs_cfg={'storage_path': 'tool_vector_store', 'index_name': 'tool'}
                     )

text = ''
for chunk in response:
    text += chunk

```

Round one:

```shell
当然可以，但是你还没有提供需要排序的数组。为了帮你完成任务，请告诉我这个数组是什么。

Action: ask_human_for_help
Action Input: {"question": "请您提供一个数组，我将对它进行排序，并找出数字4在排序后的位置。"}
请您提供一个数组，我将对它进行排序，并找出数字4在排序后的位置。
```

Then I give it an array:

```shell
[1, 2, 4, 3, 2, 1] 
```

Round two:

```shell
您提供的数组是 [1, 2, 4, 3, 2, 1]，我现在将对它进行排序。

Action: quick_sort
Action Input: {"arr": [1, 2, 4, 3, 2, 1]}
```

Round three:

```shell
排序后的数组是 [1, 1, 2, 2, 3, 4]。

Action: binary_search
Action Input: {"arr": [1, 1, 2, 2, 3, 4], "target": 4}
```

Final answer:

```shell
在排序后的数组中，数字4的位置是索引5。
```

## Quick Start

``git clone xxx``

Set your MODELSCOPE_API_TOKEN, DASHSCOPE_API_TOKEN. How to do that can refer to [modelscope-agent](https://github.com/modelscope/modelscope-agent).

``python construct_tool_vector_store.py``

``python play.py``
