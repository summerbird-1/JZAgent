import os
from typing import Dict, List, Union

from langchain.schema import Document
from langchain_community.embeddings import ModelScopeEmbeddings
from langchain_community.vectorstores import FAISS, VectorStore
from langchain_core.embeddings import Embeddings

from .base import BaseStorage


class VectorStorage(BaseStorage):

    def __init__(self,
                 storage_path: str,
                 index_name: str,
                 embedding: Embeddings = None,
                 vs_cls: VectorStore = FAISS,
                 vs_params: Dict = {},
                 index_ext: str = '.faiss',
                 use_cache: bool = True,
                 **kwargs):
        # index name used for storage
        self.storage_path = storage_path
        self.index_name = index_name
        self.embedding = embedding or ModelScopeEmbeddings(
            model_id='damo/nlp_gte_sentence-embedding_chinese-base')
        self.vs_cls = vs_cls
        self.vs_params = vs_params
        self.index_ext = index_ext
        if use_cache:
            self.vs = self.load()
        else:
            self.vs = None

    def construct(self, docs):
        assert len(docs) > 0
        if isinstance(docs[0], str):
            self.vs = self.vs_cls.from_texts(docs, self.embedding,
                                             **self.vs_params)
        elif isinstance(docs[0], Document):
            self.vs = self.vs_cls.from_documents(docs, self.embedding,
                                                 **self.vs_params)

    def search(self, query: str, top_k=5) -> List[str]:
        if self.vs is None:
            return []
        res = self.vs.similarity_search(query, k=top_k)
        if 'page' in res[0].metadata:
            res.sort(key=lambda doc: doc.metadata['page'])
        return [r.page_content for r in res]

    def add(self, docs: Union[List[str], List[Document]]):
        assert len(docs) > 0
        if isinstance(docs[0], str):
            self.vs.add_texts(docs, **self.vs_params)
        elif isinstance(docs[0], Document):
            self.vs.add_documents(docs, **self.vs_params)

    def _get_index_and_store_name(self, index_ext='.faiss', pkl_ext='.pkl'):
        index_file = os.path.join(self.storage_path,
                                  f'{self.index_name}{index_ext}')
        store_file = os.path.join(self.storage_path,
                                  f'{self.index_name}{pkl_ext}')
        return index_file, store_file

    def load(self) -> Union[VectorStore, None]:
        if not self.storage_path or not os.path.exists(self.storage_path):
            return None
        index_file, store_file = self._get_index_and_store_name(
            index_ext=self.index_ext)

        if not (os.path.exists(index_file) and os.path.exists(store_file)):
            return None

        return self.vs_cls.load_local(self.storage_path, self.embedding,
                                      self.index_name)

    def save(self):
        if self.vs:
            self.vs.save_local(self.storage_path, self.index_name)


if __name__ == '__main__':
    # tool_doc_list = ['name: "quick_sort", description: "快速排序工具，输入一个数组，返回排序后的数组。"',
    #                  'name: "binary_search", description: "二分查找工具，输入一个数组和一个目标值，返回目标值在数组中的索引。"']
    ins_vs = VectorStorage(storage_path='tool_vector_storage', index_name='tool')
    # ins_vs.construct(tool_doc_list)
    # ins_vs.save()
    # print('done')
    ins_vs.load()
    matched_tools = ins_vs.search('帮我对数组[1, 2, 3, 5, 2, 4]进行排序', top_k=1)

    match_tools_name_list = []
    import json5
    for tool in matched_tools:
        tool_name = json5.loads('{' + tool + '}')['name']
        match_tools_name_list.append(tool_name)

    print(match_tools_name_list)
