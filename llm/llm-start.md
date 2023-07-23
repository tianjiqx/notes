

## 概念

- llm(Large Language Model)：大型语言模型

- 语言模型：语言模型是一个统计模型，用于预测一段文本中下一个词或字符的概率分布。它能够学习语言的规律和结构，使得可以生成合乎语法和语义的文本。

- Tokenization（分词）：Tokenization 是将一段文本拆分成小单元（tokens）的过程。这些小单元可以是词、字符或其它更小的单元，具体取决于模型的设计和任务的要求。

- 上下文：在语言模型中，上下文是指当前词或字符出现的周围环境。上下文可以包括前面的词或字符、前几个句子、或整个文档等。模型通过上下文来进行预测和生成。

- 参数：语言模型中的参数是指模型内部的可调整变量，用于表示模型的权重和偏置。通过对参数进行训练和优化，模型能够逐渐学习到输入数据的特征和规律。

- 训练：训练是指使用大量标注数据来调整语言模型的参数，使其能够更好地预测和生成文本。在训练过程中，模型通过最小化损失函数来优化参数，使得模型的输出尽可能接近标注数据。

- 推理：推理是指在训练完成后使用训练好的语言模型来生成新的文本或进行预测。在推理过程中，模型根据输入的上下文和已生成的部分来计算下一个词或字符的概率，并选择最有可能的输出。

- Fine-tuning（微调）：Fine-tuning 是指在已经训练好的语言模型基础上，使用特定任务的数据集进行进一步的训练。通过微调，模型可以在特定任务上获得更好的性能和适应性。
  - openai fine-tuning: prompt 和 completion, 减少提问时的context, example, 经过训练, 获取应该输出的格式, 隐含背景.

- Embeddings(嵌入)：训练过程中学习到的单词或标记的向量表示。
  - 在 Prompt 加入上下文: 通过计算语料库的 Embedding，将 Vector 放到向量数据库中。然后和 Prompt 文本匹配最相似的 Vector ，并将内容放到 Prompt 中
  - 但是副作用, 有可能是不相干的材料
  - 词向量，必须使用相同的方法（模型）生成

- quantization（量化）：LLM的量化是将其高维向量表示转化为低维、离散的表示形式，以实现存储效率和计算效率的提升。
  > 将float类型参数，转为int4,int8等类型，使其在cpu上运行。

- LoRA(Low-Rank Adaptation低秩适应): 调整llm权重方法，冻结预训练模型的权重，并将可训练的秩分解矩阵注入到Transformer进行运行，避免完全重调整模型。

- Zero-shot prompting（零样本提示）：指在机器学习和自然语言处理中，使用一个模型在没有事先训练的样本示例的情况下进行推理和生成。通过给模型提供一个提示或问题，模型可以根据其先前的训练经验生成合理的输出，即使它从未在给定提示下进行过具体训练。

- Few-shot prompting（少样本提示）：类似于零样本提示，但在这种情况下，模型在给定少量示例样本的情况下进行推理和生成。通过利用少量的示例样本(n-shot通常是最频繁的n模板各自n个随机例子)，模型可以进行更准确的推理和生成，而不需要大规模的训练数据集。

- In Context Learning（上下文学习）：是一种自然语言处理技术，用于在对话或交互式环境中进行模型的在线学习。通过在对话过程中不断接收输入和反馈，并根据实时数据进行更新和调整，模型可以逐步提高其性能和适应性，以更好地满足特定任务或场景的需求。

- Instruct（指示）：在自然语言处理中，指示是一种技术或方法，用于向模型提供明确的指导或命令，以指示模型完成特定的任务。通过向模型提供特定的指示，例如问题的结构、期望的输出格式或特定的操作指令，可以引导模型生成符合预期的输出。
  - 提示（Prompts）：这是向模型提供的问题、陈述或上下文信息，用于引导回答或生成文本。提示可以是简短的问题，也可以是完整的段落。它们为模型提供了问题的背景和上下文。
  - 示例输入（Example Inputs）：这是一组用于演示模型所期望的输入格式和输出样式的样本文本。示例输入可以展示不同类型的问题、格式和回答，以帮助模型理解预期的行为。
  - 约束（Constraints）：这些是对生成文本的限制条件。约束可以是长度限制、特定词汇的使用要求、语法规则等。通过约束，可以控制模型生成的文本满足特定要求。
- RLHF（Reinforcement Learning from Human Feedback）：强化学习的范式。

- 与人类对齐（Alignment）：对回答加上人工安全限制，无害化。  

## 工具

- 模型
  - [Chinese-LLaMA-Alpaca](https://github.com/ymcui/Chinese-LLaMA-Alpaca) 中文LLaMA模型和指令精调的Alpaca大模型,在原版LLaMA的基础上扩充了中文词表并使用了中文数据进行二次预训练，进一步提升了中文基础语义理解能力。中文Alpaca模型进一步使用了中文指令数据进行精调，显著提升了模型对指令的理解和执行能力。 
  - [主流底座模型](https://github.com/Hannibal046/Awesome-LLM#open-llm) 
    - [LLaMA](https://github.com/facebookresearch/llama): meta,包含 650 亿个参数的大型语言模型。 (非常多以此为基础微调的模型) [get](https://juejin.cn/post/7209850311258898490) 并且只使用公开可用的数据集进行训练。 2023
      - [Alpaca](https://github.com/tatsu-lab/stanford_alpaca): stanford 基于LLaMA模型的指令优化
      - [Facico/Chinese-Vicuna](https://github.com/Facico/Chinese-Vicuna) 中文Vicuna模型, [Vicauna](https://lmsys.org/blog/2023-03-30-vicuna/) 在Alpaca训练方法上的改进多轮对话和扩展上下文，基于 GPT4 评分，90% 以上的回答比llama， Alpaca等更好，40%等同或更优于 chatGPT 的回答
        - [lm-sys/FastChat](https://github.com/lm-sys/FastChat)
    - [T5](https://github.com/google-research/text-to-text-transfer-transformer) - google, Text-to-Text Transfer Transformer 2019
    - [GPT](https://github.com/openai/gpt-3) 只开源到gpt3 openai lastest gpt4 2023 
    - [OPT(metaseq)](https://github.com/facebookresearch/metaseq) facebook 多语言模型  2022
    - [ChatGLM2-6B](https://github.com/THUDM/ChatGLM2-6B), [GLM](https://github.com/THUDM/GLM) 清华, 开源中英双语对话模型 2023
    - [LC1332/Luotuo-Chinese-LLM](https://github.com/LC1332/Luotuo-Chinese-LLM) Luotuo 可做following 其他中文LLM资源
    - [PaLM 2 Technical Report]() google 2023 closeSource


- 量化工具：
  - [llama.cpp](https://github.com/ggerganov/llama.cpp) llama.cpp 使用4位整数量化(quantization)运行LLaMA模型。
  - [GPTQ-for-LLaMA](https://github.com/qwopqwop200/GPTQ-for-LLaMa) 使用 GPTQ 对 LLaMA 进行 4 位量化, 只支持 linux
  

- 微调工具：
  - [peft](https://github.com/huggingface/peft)，提供加载LoRA等方法

- Bindings(指将用其他编程语言编写的库或模块封装成适用于Python编程语言的接口)
  - [llama-cpp-python](https://github.com/abetlen/llama-cpp-python)


- GPU 训练,推理加速:
  - [deepspeed](https://www.deepspeed.ai/) baichuan-7B 使用的分布式训练框架
    - [inference-tutorial](https://www.deepspeed.ai/tutorials/inference-tutorial/) 支持模型并行MP（模型分割）

- 部署运行UI
  - [text-generation-webui](https://github.com/oobabooga/text-generation-webui) 用于运行大型语言模型，如LLaMA，llama.cpp，GPT-J，Pythia，OPT和GALACTICA, 管理LoRA微调
  - [GPT4All](https://github.com/nomic-ai/gpt4all) 在 CPU 上本地运行的开源助手样式大型语言模型, 支持 GPTJ, LLaMA, MPT
  - [LangChain](https://github.com/hwchase17/langchain) 是一个用于开发由LLM驱动的应用程序的框架，旨在帮助开发人员使用LLM构建端到端的应用程序。
  - [jerryjliu/llama_index](https://github.com/jerryjliu/llama_index)
      - 提供数据连接器以引入现有数据源和数据格式（API、PDF、文档、SQL 等）
      - 结构化数据（索引、图形）(简单的向量存储索引)
      - 输入任何LLM输入提示，获取检索到的上下文和知识增强的输出
  - [vllm](https://vllm.readthedocs.io/en/latest/serving/distributed_serving.html) 支持使用ray框架，将 vLLM 扩展到单台计算机
  - [alpa](https://github.com/alpa-projects/alpa) 用于训练和服务大规模神经网络的系统,自动并行化,（基于ray管理集群）
    - [serving](https://github.com/alpa-projects/alpa/blob/main/examples/llm_serving/README.rst)

  - [InternLM/lmdeploy](https://github.com/InternLM/lmdeploy/blob/main/README_zh-CN.md) 上海人工智能实验室,openmllab 书生模型, 部署工具
  - [Hugging Face transformers](https://github.com/huggingface/transformers) 提供了数千个预训练底座模型（model hub），用于执行/组合不同模式（如文本、视觉和音频）的任务， 类似还有 [young-geng/EasyLM](https://github.com/young-geng/EasyLM)


- 应用
  - [csunny/DB-GPT](https://github.com/csunny/DB-GPT)  SQL generation and diagnosis,  text to sql
  - [Auto-GPT](https://github.com/Significant-Gravitas/Auto-GPT) chatgpt 自动化
  - [OpenLLM](https://github.com/bentoml/OpenLLM) 


## 部署

### 1.单机

text-generation-webui

多线程请求api推理

bloking_api:

/api/v1/generate： -> generate_reply 互斥锁(threading.LOCK)，逐个输出

/api/v1/chat: generate_chat_reply -> chatbot_wrapper -> generate_reply

streaming_api: (generate_params['stream'] = True) 是并发推理?依然阻塞

/api/v1/stream:  -> generate_reply 

/api/v1/chat-stream -> generate_chat_reply 

流式输出格式：a, ab,abc... ，需要skip已经输出内容。

### 2.分布式

底座模型
- 训练 
- 推理 （批量推理，并发推理）


alpa
- 批量推理，输入多个prompts, 调用 tokenizer.batch_decode （ huggingface/transformers interface）批量推理，批量输出结果。
- 支持模型： Facebook OPT系列 / [bloom](https://huggingface.co/bigscience/bloom) 多语言模型 (examples/textgen.py)  类似OPT

llama.cpp
- 支持模型：llama, Chinese llaMa/alpach, gpt4all,vicuna,baichuan-7b



vllm:
- 支持模型：LLaMA(lmsys/vicuna-13b-v1.3, young-geng/koala, openlm-research/open_llama_13b, etc)，OPT, gpt2，GPT-NeoX，（实际也支持Chinese-LLaMA-Alpaca，可能版权原因，未列出原始的llama模型）
  - [openlm-research/open_llama_13b](https://github.com/openlm-research/open_llama) 基于llama代码重新训练的权重
- 批量推理，输入多个prompts, outputs = llm.generate(prompts, sampling_params)
- api server：
    - FastAPI vllm.entrypoints.api_server
    - OpenAPI vllm.entrypoints.openai.api_server
- 分布式
  - 多 GPU 推理，--tensor-parallel-size
  - 多节点 推理， [Ray runtime](https://docs.ray.io/en/latest/ray-core/starting-ray.html)
- 缺点：
  - cpu内存（非指显卡内存）额外需求相比text-generation-webui更高，7b的13G llama 模型，单节点2 GPU（2 ray worker），消耗17G cpu内存。
  - 无上下文支持


demo：

[LLM-As-Chatbot](https://github.com/deep-diver/LLM-As-Chatbot) LLM聊天机器人服务,由于不同的模型行为不同，并且不同的模型需要不同形式的提示prompts,提供模型无关的对话和上下文管理库[Ping Pong](https://github.com/deep-diver/PingPong)
- 支持模型：Alpaca-LoRA以及衍生模型
- 上下文：支持最后保留2-3 次对话，作为prompts（更多效果不好，降低推理速度，没能缓存之前对话结果）

[openchatai/OpenChat](https://github.com/openchatai/OpenChat) 一个日常用户聊天机器人控制台,使用 GPT-3/ GPT-4，嵌入到个人网站，可简化大型语言模型的使用。

[ademakdogan/ChatSQL](https://github.com/ademakdogan/ChatSQL)  text to sql base openai ChatGPT



## 问题
### 1.模型间的区别
单轮/多轮对话(支持上下文)
上下文支持实现方式
总结prompt？来推理上下文。
流式/非流式输出结果
推理速度，checkpoint推理
语言支持能力
CPU/GPU 运行
非商业许可(llama)/商业许可(GPTJ,MPT)


## 应用开发

text to sql

- prompt（简单指令 + schema信息） + llm
- prompt + vectorStore + llm 对问题，简单向量topN召回，丰富prompts信息，vectorStore做llm的外置知识库
- prompt + nlp 预处理/ 多轮 + vectorStore + llm 传统nlp预处理和多轮任务，提高回答的准确性， 优化SQL执行效率


## REF
- [通向AGI之路：大型语言模型（LLM）技术精要](https://zhuanlan.zhihu.com/p/597586623)
- [LoRA: 大语言模型个性化的最佳实践](https://zhuanlan.zhihu.com/p/625737759)
- [大语言模型（LLM）相关学习资料整理](https://zhuanlan.zhihu.com/p/616280753)
- awesome:
  - [HqWu-HITCS/Awesome-Chinese-LLM](https://github.com/HqWu-HITCS/Awesome-Chinese-LLM) 中文底座模型，垂直领域微调及应用，数据集与教程
  - [Hannibal046/Awesome-LLM](https://github.com/Hannibal046/Awesome-LLM) 大型语言模型的精选论文列表，还包含LLM培训框架，部署LLM的工具，有关LLM的课程和教程
  - [tensorchord/Awesome-LLMOps](https://github.com/tensorchord/Awesome-LLMOps) 底座模型, 部署工具，框架
  - [kyrolabs/awesome-langchain](https://github.com/kyrolabs/awesome-langchain) langchain 学习
  - [underlines/awesome-marketing-datascience](https://github.com/underlines/awesome-marketing-datascience) 模型，工具

- Tutorials
  - [Ameet Deshpande] How Does ChatGPT Work? [Slides](https://docs.google.com/presentation/d/1TTyePrw-p_xxUbi3rbmBI3QQpSsTI1btaQuAUvvNc8w/edit#slide=id.g206fa25c94c_0_24)

  - [邱锡鹏] 大型语言模型的能力分析与应用 moss [Slides](https://github.com/Hannibal046/Awesome-LLM/blob/main/resources/%E5%A4%A7%E5%9E%8B%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B%E7%9A%84%E8%83%BD%E5%8A%9B%E5%88%86%E6%9E%90%E4%B8%8E%E5%BA%94%E7%94%A8%20-%2030min.pdf) | [Video](https://www.bilibili.com/video/BV1Xb411X7c3/?buvid=XY2DA82257CC34DECD40B00CAE8AFB7F3B43C&is_story_h5=false&mid=dM1oVipECo22eTYTWkJVVg%3D%3D&p=1&plat_id=116&share_from=ugc&share_medium=android&share_plat=android&share_session_id=c42b6c60-9d22-4c75-90b8-48828e1168af&share_source=WEIXIN&share_tag=s_i&timestamp=1676812375&unique_k=meHB9Xg&up_id=487788801&vd_source=1e55c5426b48b37e901ff0f78992e33f) 

  - [ACL 2023 Tutorial: Retrieval-based Language Models and Applications](https://acl2023-retrieval-lm.github.io/) 基于检索的语言模型

- 本地化部署,serving,

  - [GPT大语言模型Alpaca-lora本地化部署实践【大语言模型实践一】 | 京东云技术团队](https://juejin.cn/post/7233951543115186231)
  - [ray blog](https://www.anyscale.com/blog/ray-common-production-challenges-for-generative-ai-infrastructure)

  - [large-model-serving](https://github.com/tensorchord/Awesome-LLMOps#large-model-serving)


- DeepSpeed
  - [DeepSpeed 通过系统优化加速大模型推理](https://zhuanlan.zhihu.com/p/629644249)
  - [DeepSpeed + Kubernetes 如何轻松落地大规模分布式训练](https://zhuanlan.zhihu.com/p/641132519)



- 开发应用
  - [本地部署开源大模型的完整教程：LangChain + Streamlit+ Llama](https://zhuanlan.zhihu.com/p/639565332)
    - 流程：LangChain加载和转换文档 -> Embeddings -> Chroma(向量数据库) 创建存储和检索文档 -> Streamlit 构建可视化界面
  - [基于 OpenSearch 向量检索版+大模型，搭建对话式搜索](https://zhuanlan.zhihu.com/p/636966290)
    - 对话式搜索, 文档切片+向量检索+大模型生成答案（将企业数据和对话交互信息，先进行向量特征提取，然后存入向量检索引擎构建索引并进行相似度召回，将召回TOP结果传入LLM大语言模型，对信息进行对话式结果整合，最终返回给客户。） 
    - 向量检索， 优势：语义分析的向量召回
    - 业务数据：文档内容，语料，知识库，问答对

  - [万字长文：LLM应用构建全解析](https://zhuanlan.zhihu.com/p/633288551) 

  - [基于大语言模型构建知识问答系统](https://zhuanlan.zhihu.com/p/627655485)
  - [LLM+Embedding构建问答系统的局限性及优化方案](https://zhuanlan.zhihu.com/p/641132245)
    - 观点：原始语句的embedding效果不好，需要通过传统nlp处理（HanLP）生成关键词列表，然后基于关键词 Embedding，使用llm通用能力组织结果 
  - [上下文工程：基于 Github Copilot 的实时能力分析与思考](https://www.phodal.com/blog/llm-context-engineering/) 上下文工程

  - [imClumsyPanda/langchain-ChatGLM](https://github.com/imClumsyPanda/langchain-ChatGLM) 基于本地知识库的 ChatGLM 问答

  - [如何快速高效的使用 LLM 构建应用程序](https://www.cnblogs.com/botai/p/emerging-architectures.html) [原文](https://a16z.com/2023/06/20/emerging-architectures-for-llm-applications/) 
    - In-context learning: Data preprocessing / embedding -> Prompt construction / retrieval -> Prompt execution / inference 解决幻觉和数据新鲜度问题
    - agent: 解决复杂问题，对外部世界采取行动，并从部署后的经验中学习,通过结合高级推理/计划、工具使用和记忆/递归/自我反思, eg [AutoGPT](https://github.com/Significant-Gravitas/Auto-GPT) 
 
  - langchain
  - [LLMs and SQL](https://blog.langchain.dev/llms-and-sql/)
    - [crunchbot-sql-analyst-gpt](https://www.patterns.app/blog/2023/01/18/crunchbot-sql-analyst-gpt/)

  - [CVP Stack](https://zhuanlan.zhihu.com/p/642185523)  LLM+向量数据库+提示词

  - [chat2db/Chat2DB](https://github.com/chat2db/Chat2DB) 基于 openai 的java接口(com.unfbx.chatgpt) ，简单的prompt完成 sql 生成
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

  - [为什么GPT API的效果比网页版差？ - 段小草的回答 - 知乎](https://www.zhihu.com/question/606274110/answer/3089927079)    

  - [[必读] LLM 应用开发全栈指南](https://zhuanlan.zhihu.com/p/629589593), [LLM 全栈开发指南补遗](https://zhuanlan.zhihu.com/p/633033220)
    >  Retrieval [LlamaIndex原理与应用简介 bilibili](https://www.bilibili.com/video/BV1Yk4y1L7Vh/?vd_source=ffe1d2d53cd3bb3f3d39661a064bcec5) 

- 开发环境
  - [AutoDL](https://www.autodl.com/home)


- blogs
  - [快速了解 OpenAI 的 fine-tune 和 Embedding 能力](https://zhuanlan.zhihu.com/p/609359047)
  - [当LLM遇到Database：阿里达摩院联合HKU推出Text-to-SQL新基准](https://zhuanlan.zhihu.com/p/635895812)
  - [LLM学习记录（一）--关于大模型的一些知识](https://zhuanlan.zhihu.com/p/624918286)
  - [大规模语言模型（LLMs）概念篇](https://zhuanlan.zhihu.com/p/635657998) Tokenizer 


- papers
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

其他

- [prompt 提示工程](./prompt.md)

