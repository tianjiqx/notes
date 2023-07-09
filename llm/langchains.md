
## LangChians

LangChain是一个用于开发由语言模型驱动的应用程序的框架。
- Data-aware: 将语言模型连接到其他数据源
- Agentic: 让语言模型与其环境交互的工具

模块：
- MODEL I/0 与语言模型的接口
- Data connection 数据连接
    - 文档加载器
    - 文档转换（文本spliter）
    - 文档embedding models，利用第三方接口（openai等），将文本转为向量形式，
    - 向量存储
- Chains 链：对组件的一系列调用，可以包括其他链。
- Memory 持久化chains和agents的状态信息
- Agents 风装LLM对外部的操作
    - Action agents: 操作代理，适用小任务，基于之前action输出，决定下一个操作
    - Plan-and-execute agents: 计划和执行代理，预先决定完整的操作顺序（类似查询计划，DAG图）
- Callbacks： 用于日志记录、监视、流式处理等。

## REF
- [kyrolabs/awesome-langchain](https://github.com/kyrolabs/awesome-langchain) langchain 学习
- [LLMs and SQL](https://blog.langchain.dev/llms-and-sql/)
    - [crunchbot-sql-analyst-gpt](https://www.patterns.app/blog/2023/01/18/crunchbot-sql-analyst-gpt/)

