

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


## RAGFlow
英飞流公司（matrixorigin？），RAG处理系统。
亮点：

- DeepDoc
基于视觉ocr，进行文本提取，布局识别（Layout recognition），TSR（Table Structure Recognition，表结构识别） 
以及直接对图表等进行提问和处理。

- 按模板分块文档
    - book,papaer,qa,picture,

- 对应文档分块的解析器， 文档 to text
    - RAGFlowDocxParser
    - RAGFlowExcelParser
    - RAGFlowPdfParser
    - RAGFlowPptParser
    - 简历




## REF

- [基于 LangChain+LLM 的本地知识库问答：从企业单文档问答到批量文档问答](https://blog.csdn.net/v_JULY_v/article/details/131552592)
- [大模型外挂(向量)知识库](https://zhuanlan.zhihu.com/p/633671394)
    - 对称语义检索与非对称语义检索
- [Langchain-Chatchat](https://github.com/chatchat-space/Langchain-Chatchat.git) 本地知识库问答

- [infiniflow/ragflow](https://github.com/infiniflow/ragflow)
    - [DeepDoc](https://github.com/infiniflow/ragflow/blob/main/deepdoc/README_zh.md) 基于视觉ocr，进行文本提取，布局识别（Layout recognition），TSR（Table Structure Recognition，表结构识别）
        - 文本、标题、配图、配图标题、表格、表格标题
        - 页头，页尾，参考引用，公式
        - PDF、DOCX、EXCEL和PPT四种文档格式都有相应的解析器， PDF：
            - 在PDF中有自己位置的文本块（页码和矩形位置）。展示分块位置。
            - 带有PDF裁剪图像的表格，以及已经翻译成自然语言句子的内容。
            - 图中带标题和文字的图。

    - [检索增强生成引擎 RAGFlow 正式开源！](https://www.infoq.cn/article/hjjm3kv620idoyyobtps) 
    - [slides:Al 原生数据库 Infinity 系统架构与 RAG 技术实践](https://ppt.infoq.cn/slide/show?cid=143&pid=4634)

- [[合作]一次RAG技术调研](https://zhuanlan.zhihu.com/p/703596693)

- GrapRAG：处理 推理多个概念之间关系问题 
    - [微软 GraphRAG ：原理、本地部署与数据可视化——提升问答效率的图谱增强策略](https://zhuanlan.zhihu.com/p/709216702) 推荐
    - [基于 tidb 的 GraphRAG 的方式](https://zhuanlan.zhihu.com/p/709499871)
