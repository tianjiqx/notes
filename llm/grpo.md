
# GRPO 模型微调



## vllm 显存占用率计算

脚本： https://github.com/toslali-ibm/trl/blob/142f14991b43cae034ae18d1e0ae2a2f51bc1d74/scripts/recommend_gpu_util.py

在线工具：https://huggingface.co/spaces/trl-lib/recommend-vllm-memory
参数解释：

--model_config
模型的 config.json 文件路径
--exp_config
实验配置文件（YAML 格式）
--gpu_memory
单个 GPU 的总内存大小（GB，默认为 79 GB，比如 A100）
--model_params
模型参数总量（以十亿为单位，如果不提供则从模型配置中估算）
--precision_in_bytes
精度占用字节数（如 2 表示 bfloat16 或 float16）
--kv_multiplier
KV 缓存乘数（通常 K 和 V 各一份，所以默认为 2）


计算公式：

模型参数数量：假设1.5B(1B=10^9)

模型大小（Model Size）：模型大小 = 参数数 × 精度字节数 / Tensor Parallelism 大小
1.5B × 2 bytes / 1 (tp_size=1) ≈ 3 GB

KV 缓存大小（KV Cache）：
KV 缓存用于保存注意力机制中的 Key 和 Value 向量，每个 token 都需要这部分缓存。
每 token KV 缓存大小 = 2（K+V） × 层数 × (KV头数 × 隐藏层维度 / 注意力头数) × 精度字节

```
示例：

num_hidden_layers = 28
hidden_size = 1536
num_key_value_heads = 2
num_attention_heads = 12
precision = 2 bytes
每 token KV 缓存 ≈ 2 × 28 × (2 × 1536 / 12) × 2 = 16,106 字节 ≈ 0.015 MB 
```

总 KV 缓存大小：
总 KV 缓存 = 每 token KV 缓存 × batch_size × 序列长度

安全缓冲区（Buffer）：
为了防止 OOM，脚本会额外加上一个 20% 的安全缓冲：
buffer = 0.2 × (模型大小 + KV 缓存)
示例：(2.79 + 0.18) × 0.2 ≈ 0.59 GB

总内存需求：
total_required = 模型大小 + KV 缓存 + Buffer
示例：2.79 + 0.18 + 0.59 ≈ 3.56 GB

GPU 内存利用率：
GPU 内存利用率 = 总内存需求 / 单卡 GPU 内存

示例：3.56 / 79 ≈ 0.045 → 4.5%

推荐设置（向上取整到最近的 0.05 倍数）：
推荐值 = math.ceil(gpu_util_ratio * 20) / 20
示例：ceil(0.045 × 20) / 20 = 0.05 → 5% 



## REF







