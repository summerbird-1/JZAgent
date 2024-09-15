from Agent.storage.vector_storage import VectorStorage

# The tool_doc_list is just for testing. 
# Note that the last three functions are not implemented. 
# If you want to use them, you need to subclass ToolBase and register them. 
tool_doc_list = ['{name: "quick_sort", description: "快速排序工具，输入一个数组，返回排序后的数组。"}',
                '{name: "binary_search", description: "二分查找工具，输入一个数组和一个目标值，返回目标值在数组中的索引。"}',
                '{name: "ask_human_for_help", description: "用户求助工具，如果你对于要解决的任务有任何不清楚的地方，可以用这个工具向用户询问相关信息。"}',
                '{name: "get_weather", description: "天气查询工具，输入一个地点，返回该地点的天气情况。"}',
                '{name: "get_stock", description: "股票查询工具，输入一个股票代码，返回该股票的实时行情。"}',
                '{name: "get_news", description: "新闻查询工具，输入一个关键词，返回相关新闻。"}',]

ins_vs = VectorStorage(storage_path='tool_vector_store', index_name='tool')
ins_vs.construct(tool_doc_list)
ins_vs.save()

print('done')
