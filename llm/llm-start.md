

## 概念

- llm(Large Language Model)：大型语言模型

- 语言模型：语言模型是一个统计模型，用于预测一段文本中下一个词或字符的概率分布。它能够学习语言的规律和结构，使得可以生成合乎语法和语义的文本。

- Tokenization（分词）：Tokenization 是将一段文本拆分成小单元（tokens）的过程。这些小单元可以是词、字符或其它更小的单元，具体取决于模型的设计和任务的要求。

- 上下文：在语言模型中，上下文是指当前词或字符出现的周围环境。上下文可以包括前面的词或字符、前几个句子、或整个文档等。模型通过上下文来进行预测和生成。

- 参数：语言模型中的参数是指模型内部的可调整变量，用于表示模型的权重和偏置。通过对参数进行训练和优化，模型能够逐渐学习到输入数据的特征和规律。

- 训练：训练是指使用大量标注数据来调整语言模型的参数，使其能够更好地预测和生成文本。在训练过程中，模型通过最小化损失函数来优化参数，使得模型的输出尽可能接近标注数据。

- 推理：推理是指在训练完成后使用训练好的语言模型来生成新的文本或进行预测。在推理过程中，模型根据输入的上下文和已生成的部分来计算下一个词或字符的概率，并选择最有可能的输出。

- Fine-tuning（微调）：Fine-tuning 是指在已经训练好的语言模型基础上，使用特定任务的数据集进行进一步的训练。通过微调，模型可以在特定任务上获得更好的性能和适应性。

- Embeddings(嵌入)：训练过程中学习到的单词或标记的向量表示。

- quantization（量化）：将float类型参数，转为CPU友好的int4,int8等类型，使其在cpu上运行。

- LoRA(Low-Rank Adaptation低秩适应): 调整llm权重方法，冻结预训练模型的权重，并将可训练的秩分解矩阵注入到Transformer进行运行，避免完全重调整模型。

- Zero-shot prompting（零样本提示）：指在机器学习和自然语言处理中，使用一个模型在没有事先训练的样本示例的情况下进行推理和生成。通过给模型提供一个提示或问题，模型可以根据其先前的训练经验生成合理的输出，即使它从未在给定提示下进行过具体训练。

- Few-shot prompting（少样本提示）：类似于零样本提示，但在这种情况下，模型在给定少量示例样本的情况下进行推理和生成。通过利用少量的示例样本，模型可以进行更准确的推理和生成，而不需要大规模的训练数据集。

- In Context Learning（上下文学习）：是一种自然语言处理技术，用于在对话或交互式环境中进行模型的在线学习。通过在对话过程中不断接收输入和反馈，并根据实时数据进行更新和调整，模型可以逐步提高其性能和适应性，以更好地满足特定任务或场景的需求。

- Instruct（指示）：在自然语言处理中，指示是一种技术或方法，用于向模型提供明确的指导或命令，以指示模型完成特定的任务。通过向模型提供特定的指示，例如问题的结构、期望的输出格式或特定的操作指令，可以引导模型生成符合预期的输出。

- RLHF（Reinforcement Learning from Human Feedback）：强化学习的范式。


## 工具

- 模型
  - [Chinese-LLaMA-Alpaca](https://github.com/ymcui/Chinese-LLaMA-Alpaca) 中文LLaMA模型和指令精调的Alpaca大模型,在原版LLaMA的基础上扩充了中文词表并使用了中文数据进行二次预训练，进一步提升了中文基础语义理解能力。中文Alpaca模型进一步使用了中文指令数据进行精调，显著提升了模型对指令的理解和执行能力。 
  - [主流底座模型](https://github.com/Hannibal046/Awesome-LLM#open-llm) 
    - [LLaMA](https://github.com/facebookresearch/llama): meta,包含 650 亿个参数的大型语言模型。 (非常多以此为基础微调的模型) [get](https://juejin.cn/post/7209850311258898490) 并且只使用公开可用的数据集进行训练。 2023
      - [Alpaca](https://github.com/tatsu-lab/stanford_alpaca): stanford 基于LLaMA模型的指令优化
      - [GPT4All](https://github.com/nomic-ai/gpt4all) 在 CPU 上本地运行的开源助手样式大型语言模型
    - [T5](https://github.com/google-research/text-to-text-transfer-transformer) - google, Text-to-Text Transfer Transformer 2019
    - [GPT](https://github.com/openai/gpt-3) 只开源到gpt3 openai lastest gpt4 2023 
    - [OPT(metaseq)](https://github.com/facebookresearch/metaseq) facebook 多语言模型  2022
    - [ChatGLM2-6B](https://github.com/THUDM/ChatGLM2-6B), [GLM](https://github.com/THUDM/GLM) 清华, 开源中英双语对话模型 2023
    - [LC1332/Luotuo-Chinese-LLM](https://github.com/LC1332/Luotuo-Chinese-LLM) Luotuo 可做following 其他中文LLM资源
    - [PaLM 2 Technical Report]() google 2023 closeSource


- 量化工具：
  - [llama.cpp](https://github.com/ggerganov/llama.cpp) llama.cpp 目标是在MacBook上使用4位整数量化(quantization)运行LLaMA模型。
  - [GPTQ-for-LLaMA](https://github.com/qwopqwop200/GPTQ-for-LLaMa) 使用 GPTQ 对 LLaMA 进行 4 位量化, 只支持 linux

- 微调工具：
  - [peft](https://github.com/huggingface/peft)，提供加载LoRA等方法

- Bindings(指将用其他编程语言编写的库或模块封装成适用于Python编程语言的接口)
  - [llama-cpp-python](https://github.com/abetlen/llama-cpp-python)

- 部署运行UI
  - [text-generation-webui](https://github.com/oobabooga/text-generation-webui) 用于运行大型语言模型，如LLaMA，llama.cpp，GPT-J，Pythia，OPT和GALACTICA, 管理LoRA微调
  - [LangChain](https://github.com/hwchase17/langchain) 是一个用于开发由LLM驱动的应用程序的框架，旨在帮助开发人员使用LLM构建端到端的应用程序。
  - [vllm](https://vllm.readthedocs.io/en/latest/serving/distributed_serving.html) 支持使用ray框架，将 vLLM 扩展到单台计算机
  - [alpa](https://github.com/alpa-projects/alpa) 用于训练和服务大规模神经网络的系统,自动并行化,（基于ray管理集群）
    - [serving](https://github.com/alpa-projects/alpa/blob/main/examples/llm_serving/README.rst)
  - [deepspeed](https://www.deepspeed.ai/) baichuan-7B 使用的分布式训练框架

  - [Hugging Face transformers](https://github.com/huggingface/transformers) 提供了数千个预训练底座模型，用于执行不同模式（如文本、视觉和音频）的任务， 类似还有 [young-geng/EasyLM](https://github.com/young-geng/EasyLM)

## 部署

### 1.单机

text-generation-webui
多线程请求api推理
bloking_api:
/api/v1/generate： -> generate_reply 互斥锁(threading.LOCK)，逐个输出
/api/v1/chat: generate_chat_reply -> chatbot_wrapper -> generate_reply
streaming_api: (generate_params['stream'] = True) 是并发推理?
/api/v1/stream:  -> generate_reply 
/api/v1/chat-stream -> generate_chat_reply 


### 2.分布式

底座模型
- 训练 
- 推理 （批量推理，并发推理）


alpa
- 批量推理，输入多个prompt, 调用 tokenizer.batch_decode （ huggingface/transformers interface）批量推理，批量输出结果。
- 支持模型： Facebook OPT系列 / [bloom](https://huggingface.co/bigscience/bloom) 多语言模型 (examples/textgen.py)  类似OPT


[LLM-As-Chatbot](https://github.com/deep-diver/LLM-As-Chatbot) LLM聊天机器人服务
- 支持模型：Alpaca-LoRA以及衍生模型
- 支持保留2-3 次对话，作为prompts（更多效果不好，降低推理速度，没能缓存之前对话结果）

vllm:
- 支持模型：LLaMA(lmsys/vicuna-13b-v1.3, young-geng/koala, openlm-research/open_llama_13b, etc)，OPT, gpt2，GPT-NeoX
  - [openlm-research/open_llama_13b](https://github.com/openlm-research/open_llama) 基于llama代码重新训练的权重

## 问题
### 1.模型间的区别
单轮/多轮对话
流式/非流式输出结果
推理速度，checkpoint推理
语言支持能力



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

  - [邱锡鹏] 大型语言模型的能力分析与应用 Slides | Video 
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



其他

- [video: 向量数据库技术鉴赏2](https://www.bilibili.com/video/BV1BM4y177Dk) ，[向量数据库技术鉴赏1](https://www.bilibili.com/video/BV1BM4y177Dk)，chatgpt解释：
  -  Product Quantization: 用于高维向量压缩和快速相似度搜索。PQ的基本思想是将一个高维向量划分为多个子向量，并将每个子向量分别进行量化。量化过程将连续的浮点数转换为离散的码本索引。在训练阶段，PQ通过聚类算法（如k-means）将大量的训练向量划分为不同的码本（codebook）。在搜索阶段，将待查询的向量分解为子向量，并利用预先训练好的码本将每个子向量量化为码本索引。然后，通过比较查询向量的码本索引与数据库中存储的向量的码本索引来进行相似度搜索。缺点：量化过程产生信息损失。

  - HNSW（Hierarchical Navigable Small World）：用于高维向量索引的数据结构和相似度搜索算法。HNSW的基本思想是通过构建一个层级的网络结构来组织向量的索引，使得相似的向量彼此相邻，同时在每一层中使用随机连接来维持网络的"Small World"性质。
    - 在HNSW中，网络的底层是一个紧密相连的图，其中每个节点表示一个向量，并与相似的向量相连。每个节点还可以连接到上一层的节点，形成层级关系。顶层只有几个节点，通常只包含少量的向量，这些向量被称为入口点。入口点位于不同的区域，并充当整个索引结构的入口。
    - 对于查询操作，HNSW通过在网络结构中进行局部搜索来找到候选的最近邻向量，然后通过进一步的精确搜索来确定最终的最近邻。局部搜索使用跳转链接快速定位到相似的节点，而精确搜索则在候选集合中计算实际的相似度。
    - 广泛用于图像检索、文本搜索、推荐系统等领域
  - LSH（Locality Sensitive Hashing）将输入的向量映射到哈希码或哈希桶，具有相似性的向量在哈希码或哈希桶中具有较高的概率被映射到同一个位置，从而实现相似向量的局部聚集，快速相似搜索。常用：Random Projection Hashing，Bit Sampling Hashing，Multi-probe LSH。
  - 项目： [facebookresearch/Faiss](https://github.com/facebookresearch/faiss),[Milvus](https://github.com/milvus-io/milvus),[spotify/annoy](https://github.com/spotify/annoy)， [chroma-core/chroma](https://github.com/chroma-core/chroma)