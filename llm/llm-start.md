

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

## tools

- 模型
  - [Chinese-LLaMA-Alpaca](https://github.com/ymcui/Chinese-LLaMA-Alpaca) 中文LLaMA模型和指令精调的Alpaca大模型,在原版LLaMA的基础上扩充了中文词表并使用了中文数据进行二次预训练，进一步提升了中文基础语义理解能力。中文Alpaca模型进一步使用了中文指令数据进行精调，显著提升了模型对指令的理解和执行能力。
  - 主流底座模型
    - [LLaMA](https://github.com/facebookresearch/llama): meta 
    - [Alpaca](https://github.com/tatsu-lab/stanford_alpaca): stanford 基于LLaMA模型的指令优化
    - 

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

## 部署

### 1.单机



### 2.分布式
- 底座模型的模型训练 ray 
- 推理


## REF
- [通向AGI之路：大型语言模型（LLM）技术精要](https://zhuanlan.zhihu.com/p/597586623)
- [LoRA: 大语言模型个性化的最佳实践](https://zhuanlan.zhihu.com/p/625737759)
- [大语言模型（LLM）相关学习资料整理](https://zhuanlan.zhihu.com/p/616280753)
- awesome:
  - [HqWu-HITCS/Awesome-Chinese-LLM](https://github.com/HqWu-HITCS/Awesome-Chinese-LLM) 中文底座模型，垂直领域微调及应用，数据集与教程
  - [Hannibal046/Awesome-LLM](https://github.com/Hannibal046/Awesome-LLM) 大型语言模型的精选论文列表，还包含LLM培训框架，部署LLM的工具，有关LLM的课程和教程
  - [tensorchord/Awesome-LLMOps](https://github.com/tensorchord/Awesome-LLMOps) 底座模型, 部署工具
  - [kyrolabs/awesome-langchain](https://github.com/kyrolabs/awesome-langchain) langchain 学习
  - [underlines/awesome-marketing-datascience](https://github.com/underlines/awesome-marketing-datascience) 模型，工具

- 本地化部署 
 - [GPT大语言模型Alpaca-lora本地化部署实践【大语言模型实践一】 | 京东云技术团队](https://juejin.cn/post/7233951543115186231)
 - [ray blog](https://www.anyscale.com/blog/ray-common-production-challenges-for-generative-ai-infrastructure)

- 开发应用
 - [本地部署开源大模型的完整教程：LangChain + Streamlit+ Llama](https://zhuanlan.zhihu.com/p/639565332)
   - 流程：LangChain加载和转换文档 -> Embeddings -> Chroma(向量数据库) 创建存储和检索文档 -> Streamlit 构建可视化界面
 - [基于 OpenSearch 向量检索版+大模型，搭建对话式搜索](https://zhuanlan.zhihu.com/p/636966290)
   - 对话式搜索, 文档切片+向量检索+大模型生成答案（将企业数据和对话交互信息，先进行向量特征提取，然后存入向量检索引擎构建索引并进行相似度召回，将召回TOP结果传入LLM大语言模型，对信息进行对话式结果整合，最终返回给客户。） 
   - 向量检索， 优势：语义分析的向量召回
   - 业务数据：文档内容，语料，知识库，问答对

