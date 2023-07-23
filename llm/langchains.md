
## LangChians

LangChain是一个用于开发由语言模型驱动的应用程序的框架。
- Data-aware: 将语言模型连接到其他数据源
- Agentic: 让语言模型与其环境交互的工具

模块：
- MODEL I/0 与语言模型的接口
- Data connection 数据连接
    - 文档加载器
    - 文档转换（文本spliter: RecursiveCharacterTextSplitter） 
    - 文档embedding models，利用第三方接口（openai等），将文本转为向量形式，
    - 向量存储
- Chains 链：对组件的一系列调用，可以包括其他链。
- Memory 持久化chains和agents的状态信息
- Agents 风装LLM对外部的操作
    - Action agents: 操作代理，适用小任务，基于之前action输出，决定下一个操作
    - Plan-and-execute agents: 计划和执行代理，预先决定完整的操作顺序（类似查询计划，DAG图）
- Callbacks： 用于日志记录、监视、流式处理等。


#### Example selectors 示例选择器

- Select by maximal marginal relevance (MMR) MaxMarginalRelevanceExampleSelector
    - 查找嵌入与输入具有最大余弦相似性的示例，迭代添加，同时惩罚它们与已选择的示例的接近度。
- Select by similarity SemanticSimilarityExampleSelector


#### 检索

- 重复信息
    - MMR
- 冲突信息
    - 对来源进行优先级排序
- 时效性
    - 对最近的信息进行加权, 完全过滤过时的信息
    - 给生成信息带上时间戳——要求 LLM 优先选择更近期的信息
    -  人工反馈
- 元数据查询
    - 元数据过滤器，精确匹配
- 多跳问题
    - 一次提出多个问题，问题分解后多次检索
    - GPTCache 缓存 已知问题


### Agent

如何处理自然的提问，直接 prompt 工程，处理 text2sql这样问题，需要人工提供shecma,字段说明等等，非常的不自然。
此时，agent 可以分析原始问题，然后思考需要利用那些工具，来进行进一步的补充信息。


#### AgentOutputParser
代理执行输出结果处理解析，返回 AgentFinish（最终输出结果） / AgentAction（下一个链需要执行的Action， 包括需要执行工具和输入）。

- MRKLOutputParser  MRKL系统输出解析


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

- Agents 由 llm 决定 需要向向量数据库中搜索的信息
    - key1：激活 llm的 cot 能力， 第一个 prompt 对于问题的分解能力，意图的路由
    - key2：tools 的能力限制， tools 获取的准确性。



#### [chat2db/Chat2DB](https://github.com/chat2db/Chat2DB) 
基于 openai 的java接口(com.unfbx.chatgpt) ，简单的prompt完成 sql 生成

```
核心：ChatController
buildPrompt()
String schemaProperty = CollectionUtils.isNotEmpty(tableSchemas) ? String.format(
        "### 请根据以下table properties和SQL input%s. %s\n#\n### %s SQL tables, with their properties:\n#\n# "
            + "%s\n#\n#\n### SQL input: %s", pType.getDescription(), ext, dataSourceType,
        properties, prompt) : String.format("### 请根据以下SQL input%s. %s\n#\n### SQL input: %s",
        pType.getDescription(), ext, prompt);
    switch (pType) {
        case SQL_2_SQL:
            schemaProperty = StringUtils.isNotBlank(queryRequest.getDestSqlType()) ? String.format(
                "%s\n#\n### 目标SQL类型: %s", schemaProperty, queryRequest.getDestSqlType()) : String.format(
                "%s\n#\n### 目标SQL类型: %s", schemaProperty, dataSourceType);
        default:
            break;
咒语内容：给定schema（需要用户手动指定表，然后获取表的schema信息），数据库类型， prompt 说明（将自然语言转换成SQL查询, 解释SQL， 提供优化建议，进行SQL转换）
基于简单的特定指令+必要的schema信息，再无其他处理。
```


#### papers

  - [Evaluating the Text-to-SQL Capabilities of Large Language Models](https://arxiv.org/abs/2204.00498) 评估大型语言模型的文本到SQL功能
    - 结论: Codex-text2sql 是 Spider 基准上的强大基线, 基于 n-shot 的prompts 也可以泛化的其他领域,表现很好.(奇怪项目被删除/私有化了,可信度需要打?) other [itrummer/CodexDB](https://github.com/itrummer/CodexDB)
    - text to sql 的 prompts 工程 (5-shot, Create Table + Select 3) 
  - Li, Jinyang, et al. [Can LLM Already Serve as A Database Interface? A BIg Bench for Large-Scale Database Grounded Text-to-SQLs](https://arxiv.org/pdf/2305.03111.pdf). May 2023. 阿里达摩院
    - 在更多，更复杂的测试集上，text to sql，最好的ChatGPT + COT(Chain of Thought思维链)当前准确性也只有40% [bird-bench](https://bird-bench.github.io/)
    - 数据库值在为大型数据库生成准确的文本到 SQL 方面很重要（Select 3）
    - prompt： schema + 人工注释 + 外部知识（数字推理知识，领域知识，同义词知识，值说明）
    - 主要错误：
      - 错误的模式链接（41%） 将表和列错误关联
      - 误解知识证据（17%），错误复制注释内容，还可能导致sql注入风险
      - 语法错误（3%），已经是表现良好的零样本语义解析器。（其实告诉报错信息，后有一定的修正能力）

  - Gu, Zihui, et al. Few-Shot Text-to-SQL Translation Using Structure and Content Prompt Learning.




## REF
- [kyrolabs/awesome-langchain](https://github.com/kyrolabs/awesome-langchain) langchain 学习
- [LangChain 中文入门教程](https://github.com/liaokongVFX/LangChain-Chinese-Getting-Started-Guide)

- [LLMs and SQL](https://blog.langchain.dev/llms-and-sql/)
    - [crunchbot-sql-analyst-gpt](https://www.patterns.app/blog/2023/01/18/crunchbot-sql-analyst-gpt/)

- [《基于智能搜索和大模型打造企业下一代知识库》之《LangChain 集成及其在电商的应用》](https://aws.amazon.com/cn/blogs/china/intelligent-search-based-enhancement-solutions-for-llm-part-three/)
- [面向 ChatGPT 编程-可视化分析模型的探索](https://zhuanlan.zhihu.com/p/642868903)

- [大模型与数据科学：从Text-to-SQL 开始（一）](https://zhuanlan.zhihu.com/p/640580808)

- [langchain docs](https://python.langchain.com/docs/get_started)

- [LangChain 联合创始人下场揭秘：如何用 LangChain 和向量数据库搞定语义搜索？](https://link.zhihu.com/?target=https%3A//mp.weixin.qq.com/s%3F__biz%3DMzUzMDI5OTA5NQ%3D%3D%26mid%3D2247498030%26idx%3D1%26sn%3Db6c871bdf189da0dd0de6ff0c4cdb81e%26chksm%3Dfa515896cd26d180216439e4d7c5f815d299b1a53bae657d1ad3dbf8b74297cf5bd3dfc96c9e%26scene%3D21%23wechat_redirect)

- [【2023.4】思考如何设计 可靠的长文档问答系统](https://zhuanlan.zhihu.com/p/624222373)

- [HanLP《自然语言处理入门》笔记--9.关键词、关键句和短语提取](https://github.com/NLP-LOVE/Introduction-NLP)

- [大模型+知识库/数据库问答的若干问题（三）](https://zhuanlan.zhihu.com/p/642125832)


- Agent
    - [LangChain Agent 执行过程解析 OpenAI_YezIwnl 的博客](https://blog.csdn.net/qq_35361412/article/details/129797199)

    - [MRKL Systems](https://learnprompting.org/docs/advanced_applications/mrkl) MRKL系统,由一组模块（例如计算器、天气 API、数据库等）和一个路由器组成，路由器决定如何将传入的自然语言查询“路由”到相应的模块。
        - ``` 
            What is the price of Apple stock right now? 
            The current price is DATABASE[SELECT price FROM stock WHERE company = "Apple" AND time = "now"].

            What is the weather like in New York?
            The weather is WEATHER_API[New York].
          ``` 

    - [Replicating MRKL](https://python.langchain.com/docs/modules/agents/how_to/mrkl)  MRKL demo 


- [openai.Completion.create 接口参数说明](https://www.cnblogs.com/ghj1976/p/openaicompletioncreate-jie-kou-can-shu-shuo-ming.html)  stop参数用于指定在生成文本时停止生成的条件，当生成文本中包含指定的字符串或达到指定的最大生成长度时，生成过程会自动停止。
    - stop 参数在 agent 中，可以用来截断生成，插入llm推理出来的下一步Action Input，之后根据 Action Input，进入应用逻辑，执行 action，迭代推理。


- [SQL Database Agent](https://python.langchain.com/docs/modules/agents/toolkits/sql_database)  官方 SQL agent 示例，支持自然的提问提问.[sqlagent.py](./test/sqlagent.py) 做一点修改，debug。
    -  bad 情况：统计表的行数，可能生成笛卡尔积的查询语句，或者同时执行多条命令的sql。