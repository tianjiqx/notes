
# Transformer 

transformer，续写的本质
查找下一个词的本质，注意力，计算两个词之间的相关性
相关性，注意力分数，依赖一整段窗口迭代计算

自注意力机制，即注意已经输入的前置文本

模型推理（Inference）是指在训练好的模型基础上，对新的输入数据进行处理以得到预测结果的过程。

- 将输入序列送入Encoder，得到编码后的序列表示。
- 将编码后的表示和初始的输出序列（可能只是一个Start标记）送入Decoder。
- Decoder逐步生成输出序列，每次生成一个元素，并将其作为下一步的输入。
- 重复上述过程，直到生成结束标记或达到预设的最大长度。


LLM 也许是一个巨大的神谕机（hash） ，根据输入的key，获取value，只是这个key是一段话。
如何很好的提问prompt，也是如何使用好LLM的的关键。

## REF
- [译文：图解 transformer——注意力计算原理](https://mp.weixin.qq.com/s/pURSi89KAiJIJAYZ-kT-iQ)  零基础理解transformer
  - [图解 Transformer——功能概览](https://mp.weixin.qq.com/s/UJmna6_ouNzq1oiGas2Amg)
  - [图解 transformer——逐层介绍](https://mp.weixin.qq.com/s/takybSbBXkk1LC1TrUC6GQ)
  - [图解 transformer——多头注意力](https://mp.weixin.qq.com/s/Mdt55azb2ZAuxWNxTM8-mw)
  - [原文系列](https://towardsdatascience.com/transformers-explained-visually-not-just-how-but-why-they-work-so-well-d840bd61a9d3)

- Transformer/Attention Tutorial/Survey
  - [Everything You Need to Know about Transformers: Architectures, Optimization, Applications, and Interpretation, in AAAI Tutorial 2023.](https://transformer-tutorial.github.io/aaai2023/) 需要前置基础
  - 