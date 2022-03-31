
## 一致性模型





## 分类


从分布式系统、共享内存系统的角度谈一致性，假设有多个进程或处理器更新数据，如何在他们之间达成一致性。

- 强一致/严格一致性（Strict Consistency）:

  "ops in same order everywhere",难题：“network fails”，这一个一致性的最初定义是在共享内存的系统中使用,所有的处理器读到的数据都是最新的写入，这是最自然的想法和最让人愉悦的事情。在单机系统下，只允许一个写，和多读，并且读的时候不允许写，这里阻塞很严重。在分布式系统领域一致性变成所有节点所读到的数据是最新的数据,这里数据可能是共享变量，可能是数据的副本一致。比如说分布式数据库系统，为了高可用，拥有多个副本，怎么保证这些副本数是强一致的？一种常见的解决方案是设置一个主副本，只在主副本上写，然后通过raft，paxos完成数据副本间数据的一致性写。随着节点的增多，达成一致的代价，阻塞将更加严重。

- 最终一致性:

  "If no new updates to the object, **eventually** all reads will return the last updated value."，优势在于可以快速读写本地的副本，难题：“Conflicting writes”。由于最终一致性允许不读到最新数据，怎么保证不同进程的写不会冲突。

- 顺序一致性(Sequential Consistency))：

  严格一致性的弱化，不必立即看到对变量的写入，但是，所有处理器必须以相同的顺序看待不同处理器对变量的写入。线性化linearizability（也称为原子一致性atomic consistency）可以定义为有真实时间约束的顺序一致性。

- 因果一致性(Causal consistency)：
  
  顺序一致性的弱化，所有进程只要以相同的顺序查看因果相关的写操作即可。与顺序一致性一样，读取不需要即时反映更改，但是，它们需要按顺序反映对变量的所有更改。
  
- “读你所写”一致性(Read you Write Consistency)：

  特殊的因果一致性，即进程自己要看到自己的写。

- 会话一致性

- 单调读一致性

- 单调写一致性




### 参考
- [wiki: consistency model](https://en.wikipedia.org/wiki/Consistency_model),详细的一致性类型介绍介绍
- [Consistency models in modern distributed systems. An approach to Eventual Consistency](https://riunet.upv.es/bitstream/handle/10251/54786/TFMLeticiaPascual.pdf)
- [Consistency Models](https://jepsen.io/consistency),jepsen
- 《大数据日知录》2.2节
- [线性一致性：什么是线性一致性？](https://zhuanlan.zhihu.com/p/42239873)
- [分布式线性一致性：理论&验证](https://zhuanlan.zhihu.com/p/43949695)
- [distributed-consensus-reading-list](https://github.com/heidihoward/distributed-consensus-reading-list)





