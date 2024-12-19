# LLM 微调

## 工具

LLaMA-Factory是一个不错的微调工具。AutoDL 上也有有一个镜像[hiyouga/LLaMA-Factory/LLaMA-Factory](https://www.codewithgpu.com/i/hiyouga/LLaMA-Factory/LLaMA-Factory)，可能较旧需要自己做一定的更新。B站有其使用说明，不过主要有用的地方在于基本的依赖已经安装好，无需自己安装、编译cuda等

- [LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory)


AutoDL Tips：
- 支持无卡运行，配置环境时省钱
- 西北区资源更多，并且主要允许磁盘扩容


## 微调参数

- learn_rating 学习率
  - 1e-4  -> 1e-5 学习率降低，欠拟合，告警规则学习效果变差，最后loss增加
  - 1e-4 -> 7e-4 学习率增加，学习效果增加
(learn_rating 学习更低，模型会更加稳定，大规模语料时，一般建议原始模型预训练或者微调的学习率0.1，qwen2.5 其实是 7e-6~7e-7
个人使用发现,对于长文本的小数据（35base case * 50）对于 qwen2.5-7B，32B 模型 3e-4 训练效果较好)

- epoch 迭代次数
  - 1 -> 8  增强了拟合效果，提升了输出按照语料的内容输出能力
  - 当微调数据量少时，就需要多个epoch训练，降低loss，一般而言至少应该低于1，更多epoch降低到0.00x级别。

- lora_dropout 0 dropout参数设置成0, 更好的学习
- use_rslora ture 秩稳定，确保输出结果更好，避免产生中英、间繁，全角、半角等。
- shift_attn true  longlora，长文本预料 
- flash_attn fa2 加速微调训练
- lora_rank 32， 调大秩，对输入特征具有更多，但是训练参数增加，显存消耗也会增加
- lora_alpha 128
- cutoff_len 4096 预料输入长度限制，扩大，也会增加显存消耗

- 微调时，可以调整 LLM 参数 (效果其实不大)，修改模型加载的默认生成参数配置（../models/Qwen2.5-14B-Instruct-GPTQ-Int4/generation_config.json）
    - temperature
    - top_p
    - top_k



## 语料

扩充语料：

- 扩展语料，单个选项
- 增加内容解释的语料
- 调整角色设定 {你是一位资深的电力系统分析师，拥有电气工程领域的硕士或更高学位，具备多年电网监控和故障分析经验。}
- 补充语料的逻辑和内容分析，结合变种语料
- 拆分prompt，任务
- Q&A交换，逆否语料
- 根据内容，判断正确错误，解释等

（预料拆分，可能对于大的模型，导致微调产生歧义， 对于大的模型， 单预料足够高即可）

## 合并 & 量化

可以先简单合并lora，之后量化。

bitsandbytes 确实推理更慢，并且 vllm 暂时支持的不好，最新版本vllm（0.6.5）开始支持，但是whl缺少。
建议还是GPTQ量化，再使用vllm加速推理。

- [LLM量化方法对比: GPTQ VS bitsandbytes](https://zhuanlan.zhihu.com/p/690821357)

## 评估 

- all-MiniLM-L12-v2  语义相似性度量 (微调而言判断可能不佳)
- ROUGE 分数，计算ROUGE-L超过0.99的比例
    - ROUGE-1 主要关注单个词的重叠情况。
    - ROUGE-2 关注两个连续词的重叠情况。
    - ROUGE-L 关注最长公共子序列的重叠情况，通常能更好地捕捉文本的语义信息。


## 经验总结

- 优先大模型，比如Qwen2.5-32B-Instruct
- 7B小模型，对于短QA，可以较好的学习
- 依赖问题，总是有torch各种undefined symbol时，一些依赖库，建议可以使用源码安装（pip install -e .）。
- 长文本输出存在中英、间繁，全角、半角等问题，建议提升模型
- 需要在非量化模型上微调
    - 但是实际可以量化模型微调，然后与非量化模型合并，对合并后的模型做量化（效果未知）。


## REF
- [李乾坤：LLM微调理论](https://qiankunli.github.io/2023/10/29/llm_finetune_theory.html)
- [李乾坤：LLM微调实践](https://qiankunli.github.io/2024/07/28/llm_finetune_practice.html#%E9%95%BF%E6%96%87%E6%9C%AC)
- [大模型微调经验和认知](https://mp.weixin.qq.com/s/lYJcnUW9qtTsAF7_G8)

- [AGI掘金知识库](https://agijuejin.feishu.cn/wiki/EtoiwSfomiHnmukOCDncsdnenYd) 一些blog






