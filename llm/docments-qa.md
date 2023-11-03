

## 文档问答/本地知识库问答


- 文档加载器
    - image：UnstructuredImageLoader（langchain）， RapidOCRLoader  （Langchain-Chatchat）基于rapidocr_onnxruntime的 RapidOCR， 识别图片中的文字，转为文档
    - pdf： UnstructuredPDFLoader, PyPDFLoader （langchain）， RapidOCRPDFLoader（Langchain-Chatchat） 
    - docs：Docx2txtLoader （langchain）
    - html: UnstructuredHTMLLoader（langchain）
    - json, markdown, txt, csv（langchain）
- 文档切分
    - langchian  
        - CharacterTextSplitter
        - RecursiveCharacterTextSplitter
        - MarkdownTextSplitter
        
    - Langchain-Chatchat
        - AliTextSplitter （Langchain-Chatchat） 文档语义分割模型，达摩院开源的nlp_bert_document-segmentation_chinese-base 
        - ChineseRecursiveTextSplitter
- 文档索引
    - Vector， 文件先切分为 Chunks，在按 Chunks 分别编码存储并检索
        - indexing LangChain 索引 API, 避免将重复的内容写入矢量存储，避免重写未更改的内容，免在未更改的内容上重新计算embeddings
    - KG，利用 LLM 抽取文件中的三元组，将其存储为 KG 供后续检索
- Vector 提取器
    - 基于关键字的检索：使用关键字匹配来查找相关文档
    - 基于embedding方法：使用预训练的神经网络模型（如 BERT、RoBERTa 等）将文档和查询编码为向量，并进行相似度计算
        - MultiQueryRetriever （langchain）通过使用 MultiQueryRetriever LLM 从不同角度为给定的用户输入查询生成多个查询，从而自动执行提示优化过程。AIOps的目标是什么？['1. AIOps的主要目标是什么？', '2. 如何通过AIOps实现目标？', '3. AIOps与其他IT运维工具相比，有哪些独特的目标？']  什么是智能运维？ ['1. 智能运维的定义是什么？', '2. 如何实现智能运维？', '3. 智能运维的优势和应用场景有哪些？']
        - ContextualCompressionRetriever 上下文压缩，减少文档内容或完全删除文档来缩短文档
        - MultiVector 为每个文档创建多个向量，较小的块，摘要，假设性问题：创建每个文档适合回答的假设性问题，将这些问题与文档一起嵌入（或代替）文档
    - 索引方法：例如倒排索引，这是搜索引擎常用的技术，可以快速找到包含特定词或短语的文档
    - 混合，以提高检索的准确性和速度

- LLM 总结 TOP-K




## REF

- [基于 LangChain+LLM 的本地知识库问答：从企业单文档问答到批量文档问答](https://blog.csdn.net/v_JULY_v/article/details/131552592)
- [大模型外挂(向量)知识库](https://zhuanlan.zhihu.com/p/633671394)
    - 对称语义检索与非对称语义检索
- [Langchain-Chatchat](https://github.com/chatchat-space/Langchain-Chatchat.git) 本地知识库问答



