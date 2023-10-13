
## 向量数据库

-  [facebookresearch/Faiss](https://github.com/facebookresearch/faiss) 
    langchin python 版本，全内存
- [lancedb](https://github.com/lancedb/lancedb) 基于 lance 格式存储的 向量数据库
    - 支持 multi-modal data (text, images, videos, point clouds, and more) 
    - similarity search, full-text search and SQL.
    - rust



内存空间需求：

数据集 Sift1M  100万，128维, 总计 1 GB

float32 4B 
向量图： 1,000,000 x 128 x 4 bytes = 512,000,000   512MB 
邻域图：索引时还会构建邻域的图形表示。该图表示每个向量的 k 最近邻。
int64 标识
1,000,000 x 64 x 8 bytes = 512,000,000 bytes  512MB



### 维度
- 部署（self-hosted / cloud / in-memory） 
- Metadata Filtering
- Hybrid Search （向量/标量搜索）
- Delete
- 持久化（WAL）
- Async 异步 / GPU
- 开源

## REF
- [video: 向量数据库技术鉴赏2](https://www.bilibili.com/video/BV1BM4y177Dk) ，[向量数据库技术鉴赏1](https://www.bilibili.com/video/BV1BM4y177Dk)，chatgpt解释：
  -  Product Quantization: 用于高维向量压缩和快速相似度搜索。PQ的基本思想是将一个高维向量划分为多个子向量，并将每个子向量分别进行量化。量化过程将连续的浮点数转换为离散的码本索引。在训练阶段，PQ通过聚类算法（如k-means）将大量的训练向量划分为不同的码本（codebook）。在搜索阶段，将待查询的向量分解为子向量，并利用预先训练好的码本将每个子向量量化为码本索引。然后，通过比较查询向量的码本索引与数据库中存储的向量的码本索引来进行相似度搜索。缺点：量化过程产生信息损失。

  - HNSW（Hierarchical Navigable Small World）：用于高维向量索引的数据结构和相似度搜索算法。HNSW的基本思想是通过构建一个层级的网络结构来组织向量的索引，使得相似的向量彼此相邻，同时在每一层中使用随机连接来维持网络的"Small World"性质。
    - 在HNSW中，网络的底层是一个紧密相连的图，其中每个节点表示一个向量，并与相似的向量相连。每个节点还可以连接到上一层的节点，形成层级关系。顶层只有几个节点，通常只包含少量的向量，这些向量被称为入口点。入口点位于不同的区域，并充当整个索引结构的入口。
    - 对于查询操作，HNSW通过在网络结构中进行局部搜索来找到候选的最近邻向量，然后通过进一步的精确搜索来确定最终的最近邻。局部搜索使用跳转链接快速定位到相似的节点，而精确搜索则在候选集合中计算实际的相似度。
    - 广泛用于图像检索、文本搜索、推荐系统等领域
  - LSH（Locality Sensitive Hashing）将输入的向量映射到哈希码或哈希桶，具有相似性的向量在哈希码或哈希桶中具有较高的概率被映射到同一个位置，从而实现相似向量的局部聚集，快速相似搜索。常用：Random Projection Hashing，Bit Sampling Hashing，Multi-probe LSH。
  - 项目： [facebookresearch/Faiss](https://github.com/facebookresearch/faiss),[Milvus](https://github.com/milvus-io/milvus),[spotify/annoy](https://github.com/spotify/annoy)， [chroma-core/chroma](https://github.com/chroma-core/chroma)

- [语义索引（向量检索）的几类经典方法](https://zhuanlan.zhihu.com/p/161467314)
- [高维空间最近邻逼近搜索算法评测](https://zhuanlan.zhihu.com/p/37381294) 
  - [erikbern/ann-benchmarks](https://github.com/erikbern/ann-benchmarks)


- Weaviate
  - [Vamana vs. HNSW - Exploring ANN algorithms Part 1](https://weaviate.io/blog/ann-algorithms-vamana-vs-hnsw)
  - [HNSW+PQ - Exploring ANN algorithms Part 2.1](https://weaviate.io/blog/ann-algorithms-hnsw-pq)

- [llamaindex vector stores](https://gpt-index.readthedocs.io/en/latest/core_modules/data_modules/storage/vector_stores.html)

- [矢量数据库对比和选择指南](https://zhuanlan.zhihu.com/p/641822949)
- [Milvus 、Qdrant、Waeviate、Pinecone、ElasticSearch矢量数据库对比](https://zhuanlan.zhihu.com/p/641268774)