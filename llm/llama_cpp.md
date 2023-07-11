
## llama.cpp CPU量化工具

Facebook 的 LlaMA 

1. 构建
按照 readme 提示，下载，然后 make 安装。

# install Python dependencies
python3 -m pip install -r requirements.txt


# obtain the original LLaMA model weights and place them in ./models
ls ./models
65B 30B 13B 7B tokenizer_checklist.chk tokenizer.model


7B
```
consolidated.00.pth pytorch模型文件
params.json   
checklist.chk   md5sum

```


2. 使用

```
# convert the 7B model (consolidated.00.pth) to ggml FP16 format (ggml-model-f16.bin)
python3 convert.py models/7B/

# quantize the model to 4-bits (using q4_0 method)
./quantize ./models/7B/ggml-model-f16.bin ./models/7B/ggml-model-q4_0.bin q4_0

# run the inference
./main -m ./models/7B/ggml-model-q4_0.bin -n 128

```


## REF

- https://github.com/ggerganov/llama.cpp

