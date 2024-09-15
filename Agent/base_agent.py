from abc import ABC, abstractmethod
from typing import Dict, Iterator, List, Optional, Tuple, Union

from Agent.llm import get_chat_model
from Agent.llm.base import BaseChatModel
from Agent.tools import TOOL_REGISTRY
from Agent.utils.utils import has_chinese_chars

import json5


class BaseAgent(ABC):

    def __init__(self,
                 function_list: Optional[List[Union[str, Dict]]] = None,
                 llm: Optional[Union[Dict, BaseChatModel]] = None,
                 storage_path: Optional[str] = None,
                 name: Optional[str] = None,
                 description: Optional[str] = None,
                 instruction: Union[str, dict] = None,
                 **kwargs):
        """
        init tools/llm/instruction for one agent

        Args:
            function_list: A list of tools
                (1)When str: tool names
                (2)When Dict: tool cfg
            llm: The llm config of this agent
                (1) When Dict: set the config of llm as {'model': '', 'api_key': '', 'model_server': ''}
                (2) When BaseChatModel: llm is sent by another agent
            storage_path: If not specified otherwise, all data will be stored here in KV pairs by memory
            name: the name of agent
            description: the description of agent, which is used for multi_agent
            instruction: the system instruction of this agent
            kwargs: other potential parameters
        """
        # assign a model to the agent given config or an instantiated model
        if isinstance(llm, Dict):
            self.llm_config = llm
            self.llm = get_chat_model(**self.llm_config)
        else:
            self.llm = llm

        self.stream = True

        # register and instantiate tools into function_map
        self.function_list = []
        self.function_map = {}
        if function_list:
            for function in function_list:
                self._register_tool(function)

        self.storage_path = storage_path
        self.mem = None
        self.name = name
        self.description = description
        self.instruction = instruction
        self.uuid_str = kwargs.get('uuid_str', None)

    def run(self, *args, **kwargs) -> Union[str, Iterator[str]]:
        if 'lang' not in kwargs:
            if has_chinese_chars([args, kwargs]):
                kwargs['lang'] = 'zh'
            else:
                kwargs['lang'] = 'en'
        
        if kwargs.get('use_vs', None) is not None:
            use_vs = kwargs['use_vs']
            if use_vs:
                if kwargs.get('vs_cfg', None) is None:
                    raise ValueError('Please specify the vs_cfg when use_vs is True')
                
                vs_cfg = kwargs['vs_cfg']
                from Agent.storage.vector_storage import VectorStorage
                if getattr(self, 'function_retriever', None) is None:
                    if vs_cfg.get('index_name') is None:
                        vs_cfg['index_name'] = 'tool'
                    self.function_retriever = VectorStorage(**vs_cfg,)
                    self.function_retriever.load()
            
            if use_vs:
                matched_tools = self.function_retriever.search(args[0], top_k=2)
                function_list = []
                for tool in matched_tools:
                    tool_name = json5.loads(tool)['name']
                    function_list.append(tool_name)
                if function_list:
                    for function in function_list:
                        self._register_tool(function)

        return self._run(*args, **kwargs)

    @abstractmethod
    def _run(self, *args, **kwargs) -> Union[str, Iterator[str]]:
        raise NotImplementedError

    def _call_llm(self,
                  prompt: Optional[str] = None,
                  messages: Optional[List[Dict]] = None,
                  stop: Optional[List[str]] = None,
                  **kwargs) -> Union[str, Iterator[str]]:
        return self.llm.chat(
            prompt=prompt,
            messages=messages,
            stop=stop,
            stream=self.stream,
            **kwargs)

    def _call_tool(self, tool_name: str, tool_args: str, **kwargs):
        """
        Use when calling tools in bot()

        """
        return self.function_map[tool_name].call(tool_args, **kwargs)

    def _register_tool(self, tool: Union[str, Dict]):
        """
        Instantiate the global tool for the agent

        Args:
            tool: the tool should be either in a string format with name as value
            and in a dict format, example
            (1) When str: amap_weather
            (2) When dict: {'amap_weather': {'token': 'xxx'}}

        Returns:

        """
        tool_name = tool
        tool_cfg = {}
        if isinstance(tool, dict):
            tool_name = next(iter(tool))
            tool_cfg = tool[tool_name]
        if tool_name not in TOOL_REGISTRY:
            raise NotImplementedError
        if tool not in self.function_list:
            self.function_list.append(tool)
            tool_class = TOOL_REGISTRY[tool_name]
            try:
                self.function_map[tool_name] = tool_class(tool_cfg)
            except TypeError:
                # When using OpenAPI, tool_class is already an instantiated object, not a corresponding class
                self.function_map[tool_name] = tool_class
            except Exception as e:
                raise RuntimeError(e)
            
            if self.llm.model_server == 'openai':
                self.function_map[tool_name].schema = 'oai'
            else:
                self.function_map[tool_name].schema = ''
