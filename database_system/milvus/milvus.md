
# Milvus


特性：

- 支持嵌入式版本 Milvus lite （部分特性还不支持，计划是完全支持，比如全文检索）
- [全文检索](https://milvus.io/docs/full-text-search.md) 基于BM25 实现的稀疏索引
- 混合搜索：全文搜索与基于语义的密集向量搜索集成


## REF

- [docs-zh:milvus](https://milvus.io/docs/zh)
    - [bootcamp](https://milvus.io/bootcamp) Tutorials
- [Milvus：A Purpose-Built Vector Data Management System](https://zhuanlan.zhihu.com/p/536418778)
- [Milvus 开源向量数据库-知乎专栏](https://www.zhihu.com/column/ai-search) 
- [langchain + milvus](https://python.langchain.com/docs/integrations/vectorstores/milvus/)
- blogs:
    - [探索BGE-M3和Splade：两种用于生成稀疏嵌入的机器学习模型](https://zilliz.com/learn/bge-m3-and-splade-two-machine-learning-models-for-generating-sparse-embeddings)
    - [SPLADE稀疏向量与BM 25的比较](https://zilliz.com/learn/comparing-splade-sparse-vectors-with-bm25)
        - 最佳匹配25（BM 25）是一种文本匹配算法，可视为词频-逆文档频率（TF-IDF）算法的增强。TF-IDF是一种信息检索算法，用于测量文档中关键字相对于文档集合的重要性。
            - 传统的TF-IDF算法没有考虑文档的长度。这导致较长的文档比较短的文档具有优势，因为关键字出现更频繁的可能性随着文档长度的增加而增加。BM 25算法通过规范化术语频率（TF）方程中的文档长度来解决这个问题。
            - BM 25算法中的饱和项通过随着关键字出现频率的增加而逐渐减少关键字出现的影响来解决这个问题。
        - SPLADE能够捕获语义相似的术语，即使没有精确的关键字匹配，也可以为给定的查询检索更多相关的文档。