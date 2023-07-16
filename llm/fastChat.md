## FastChat

支持 cpu / GPU 部署模型

- [支持模型](https://github.com/lm-sys/FastChat/blob/main/docs/model_support.md)

- [支持训练lora](https://github.com/lm-sys/FastChat/blob/main/docs/training.md) 使用 deepspeed 


结论：由于使用 HF 的原始模型而非量化，进行推理，使用消费级的CPU进行推理，基本不可用。（24核的商业服务器稍好，CPU可以在分钟内给出结果）


```

# 参数
--device cpu  使用运行 cpu
--load-8bit  量化，减少内存消耗


# cli
python3 -m fastchat.serve.cli --model-path lmsys/vicuna-7b-v1.3 --device cpu --load-8bit 

# restful worker 
python3 -m fastchat.serve.model_worker --model-names "gpt-3.5-turbo,text-davinci-003,text-embedding-ada-002" --model-path lmsys/vicuna-7b-v1.3 --device cpu --load-8bit 



```



## langchins 集成

原理包装成服务 openai 服务供 langchains 使用。

1. 启动本地fastchat 的 RESTful API 服务

```
python3 -m fastchat.serve.controller

python3 -m fastchat.serve.model_worker --model-names "gpt-3.5-turbo,text-davinci-003,text-embedding-ada-002" --model-path lmsys/vicuna-7b-v1.3 --device cpu --load-8bit 

python3 -m fastchat.serve.openai_api_server --host localhost --port 8000

```
2. 设置 open ai env

```
export OPENAI_API_BASE=http://localhost:8000/v1
export OPENAI_API_KEY=""


```

3. langchins 程序 配置 open ai 模型


demo case 一些坑：

1.命令行配置了代理（http_proxy），报错：
ImportError: Using SOCKS proxy, but the 'socksio' package is not installed. Make sure to install httpx using `pip install httpx[socks]`.
需要安装 `pip install socksio`

2. pip install chromadb 导致 pydantic 降级，导入openai报错
需要手动恢复回 `pip install pydantic==1.10.11 `

3. 请求超时，默认100， 需要设置更大
export FASTCHAT_WORKER_API_TIMEOUT=1000

state_of_the_union.txt 减少文本量


langchains demo 例子
```
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator

import os

# 设置环境变量
# OPENAI_API_KEY=sk-UjRJKjGVOKzxxxxxtOoJcw655VCT
os.environ['OPENAI_API_KEY'] = "EMPTY"
os.environ['OPENAI_API_BASE'] = "http://localhost:8000/v1"

print(os.environ['OPENAI_API_KEY'])
print(os.environ['OPENAI_API_BASE'])

embedding = OpenAIEmbeddings(model="text-embedding-ada-002")

#from langchain.embeddings import HuggingFaceEmbeddings
#embedding = HuggingFaceEmbeddings()

loader = TextLoader("state_of_the_union.txt")
index = VectorstoreIndexCreator(embedding=embedding).from_loaders([loader])
llm = ChatOpenAI(model_name="vicuna-7b-v1.3")
questions = [
    "Who is the speaker",
    "What did the president say about Ketanji Brown Jackson",
    "What are the threats to America",
    "Who are mentioned in the speech",
    "Who is the vice president",
    "How many projects were announced",
]

for query in questions:
    print("Query:", query)
    print("Answer:", index.query(query, llm=llm))


```


```
// 基本失败， 回答效果不好，还是，推理超时 httpcore.ReadTimeout
Query: Who is the speaker
huggingface/tokenizers: The current process just got forked, after parallelism has already been used. Disabling parallelism to avoid deadlocks...
To disable this warning, you can either:
	- Avoid using `tokenizers` before the fork if possible
	- Explicitly set the environment variable TOKENIZERS_PARALLELISM=(true | false)
Retrying langchain.chat_models.openai.ChatOpenAI.completion_with_retry.<locals>._completion_with_retry in 1.0 seconds as it raised APIError: Invalid response object from API: '{"object":"error","message":"","code":50001}' (HTTP response code was 400).
Answer: The speaker mentioned in the text is not specified.
Query: What did the president say about Ketanji Brown Jackson
Retrying langchain.chat_models.openai.ChatOpenAI.completion_with_retry.<locals>._completion_with_retry in 1.0 seconds as it raised APIError: Invalid response object from API: '{"object":"error","message":"","code":50001}' (HTTP response code was 400).
Retrying langchain.chat_models.openai.ChatOpenAI.completion_with_retry.<locals>._completion_with_retry in 2.0 seconds as it raised APIError: Invalid response object from API: 'Internal Server Error' (HTTP response code was 500).

```

4. 简单问答

```

curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-3.5-turbo",
    "messages": [{"role": "user", "content": "Hello! What is your name?"}]
  }'

{"id":"chatcmpl-CrZGKVjTZaS9msJLk65pmS","object":"chat.completion","created":1689087615,"model":"gpt-3.5-turbo","choices":[{"index":0,"message":{"role":"assistant","content":"Hello! I'm a language model called Vicuna, and I'm trained by researchers from Large Model Systems Organization (LMSYS)."},"finish_reason":"stop"}],"usage":{"prompt_tokens":46,"total_tokens":78,"completion_tokens":32}}


curl http://localhost:8000/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-3.5-turbo",
    "prompt": "Once upon a time",
    "max_tokens": 41,
    "temperature": 0.5
  }'

curl http://localhost:8000/v1/embeddings \
  -H "Content-Type: application/json" \
  -d '{
    "model": "text-embedding-ada-002",
    "input": "Hello world!"
  }'



```


### REF
- https://github.com/lm-sys/FastChat/blob/main/docs/langchain_integration.md




