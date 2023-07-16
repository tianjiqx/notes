
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


### openai
```
import openai
from langchain.llms import OpenAI
from langchain import PromptTemplate, LLMChain
import os

# 设置环境变量
os.environ['OPENAI_API_KEY'="sk-UjRJKjxxxxxxqGtOoJcw655VCT" # your key
# 设置代理
os.environ["OPENAI_PROXY"] = "http://127.0.0.1:7890"

# print(openai.Model.list())

llm = OpenAI()

res = llm.predict("What would be a good company name for a company that makes colorful socks?")
print(res)

```

### Text to SQL-Like

目标 text to 类SQL的查询语言。经过测试，在prompt中提供直接提供语法规则说明效果并不理想。
而是提供一定的5-10条示例，能够有较好的效果。(少样本学习)

少样本学习，关键： 
- 根据问题，向问题集库中，搜索相似的问题和回答 [Select by maximal marginal relevance]](https://python.langchain.com/docs/modules/model_io/prompts/example_selectors/mmr)

- 提升相似搜索的正确性，补充文档相关的文档 llamaindex


## REF
- [kyrolabs/awesome-langchain](https://github.com/kyrolabs/awesome-langchain) langchain 学习
- [LLMs and SQL](https://blog.langchain.dev/llms-and-sql/)
    - [crunchbot-sql-analyst-gpt](https://www.patterns.app/blog/2023/01/18/crunchbot-sql-analyst-gpt/)

- [《基于智能搜索和大模型打造企业下一代知识库》之《LangChain 集成及其在电商的应用》](https://aws.amazon.com/cn/blogs/china/intelligent-search-based-enhancement-solutions-for-llm-part-three/)
- [面向 ChatGPT 编程-可视化分析模型的探索](https://zhuanlan.zhihu.com/p/642868903)

- [大模型与数据科学：从Text-to-SQL 开始（一）](https://zhuanlan.zhihu.com/p/640580808)

- [langchain docs](https://python.langchain.com/docs/get_started)
