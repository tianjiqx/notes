
## chat4all

最简单尝试llm

langchain + chat4all

对话问答 demo:

下载: nous-hermes-13b.ggmlv3.q4_0.bin, 还有其他int4量化的可在cpu上执行的模型
https://gpt4all.io/index.html  Model Explorer 


Hugging Face ggml 量化模型搜索：
https://huggingface.co/models?other=ggml&sort=trending
（建议通过motrix加速下载）




限制：
不支持 中文llama量化模型


### 安装
```shell
conda activate llm

pip install langchain
pip install gpt4all

```

### 代码
```python
from langchain import PromptTemplate, LLMChain
from langchain.llms import GPT4All
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

import datetime
import time

class Timer(object):
    """
    计时器，记录执行耗时
    """

    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, *args):
        self.end = time.perf_counter()
        self.interval = self.end - self.start


current_time = datetime.datetime.now()
print("Current time：", current_time)

template = """Question: {question}

Answer: Let's think step by step."""

prompt = PromptTemplate(template=template, input_variables=["question"])

local_path = (
    "/home/tianjiqx/Downloads/llm/nous-hermes-13b.ggmlv3.q4_0.bin"  # replace with your desired local file path
)


# Callbacks support token-wise streaming
callbacks = [StreamingStdOutCallbackHandler()]

llm_chain = None
with Timer() as t:
    # Verbose is required to pass to the callback manager
    llm = GPT4All(model=local_path, callbacks=callbacks, verbose=True)
    # If you want to use a custom model add the backend parameter
    # Check https://docs.gpt4all.io/gpt4all_python.html for supported backends
    #llm = GPT4All(model=local_path, backend="gptj", callbacks=callbacks, verbose=True)
    llm_chain = LLMChain(prompt=prompt, llm=llm)
print('load model: spend time {:.3f} s'.format(t.interval))    

current_time = datetime.datetime.now()
print("Current time：", current_time)
# question = "What NFL team won the Super Bowl in the year Justin Bieber was born?"
# question = "介绍一下秦始皇, 用中文输出"
#
# print(question)
# with Timer() as t:
#     llm_chain.run(question)
# print('\nrun question: spend time {:.3f} s'.format(t.interval))


while True:
    question = input("Enter something questions (or 'q' to quit): ")
    if question == 'q':
        break
    print("You entered:", question)
    with Timer() as t:
        llm_chain.run(question)
    print('\nRun question: spend time {:.3f} s'.format(t.interval))

print('end!')
```

### 效果:


// nous-hermes-13b.ggmlv3.q4_0.bin

// 1
What NFL team won the Super Bowl in the year Justin Bieber was born?
 In 1994, Justin Bieber was not yet born (he was born on March 1st, 1994). 
 The first Super Bowl of that year took place on January 23rd, 
 where the San Francisco 49ers defeated the Dallas Cowboys with a score of 55-10. 
 So, in the year Justin Bieber was born (1994), the NFL team that won the Super Bowl was the San Francisco 49ers.
run question: spend time 22.447 s


// 2
介绍一下秦始皇
llama_new_context_with_model: kv self size  = 1600.00 MB
 Qin Shi Huang was the first emperor of China, who unified China and laid the foundation for its future development. 
 He is best known for his political reforms, military conquests, and building projects that helped to shape ancient Chinese civilization.

Qin Shi Huang came into power in 246 BC after defeating several rival states. To consolidate his rule, he implemented a series of political reforms aimed at centralizing the government and strengthening its authority over the people. One of these reforms was to standardize the writing system by creating a unified set of characters known as "small seal script."

In addition to political reforms, Qin Shi Huang also focused on military conquests. He expanded his empire through aggressive campaigns against neighboring states and conquered territories that would become part of China's core regions. His most famous military achievement was the unification of warring kingdoms under a centralized government, which laid the foundation for the formation of modern-day China.

Qin Shi Huang is also remembered for his ambitious building projects, including the construction of the Great Wall and the Terracotta
run question: spend time 95.860 s


// 3
介绍一下秦始皇, 用中文输出
 Firstly, we need to convert the English name "Qin Shi Huang" into Chinese characters using pinyin system. 
 The pronunciation of each character in pinyin is as follows: Qín (���), Shì (始), Húang (皇).

Now let's output these characters one by one:

1. ��� (Qín): Type "Q" and press Enter, then type "i" and press Enter again, finally type "n" and press Enter to complete the character.
2. 始 (Shì): Same as above, type "S", "h", "i". Press Enter for each letter. Then type "i" and press Enter one more time to complete the character.
3. 皇 (Húang): Type "H", "u", "a", "n". Press Enter for each letter. Finally, type "g" and press Enter again to complete the character.
run question: spend time 58.917 s


// 4

You entered: who are you?
 First, I am a computer program that can answer questions. Second, my answers come from the information stored in my database. Third, this information is compiled and curated by humans. Fourth, these humans work for the company that created me to ensure accuracy and relevance. Finally, you could say that I am an artificial intelligence powered by human knowledge. So, who are you?
Run question: spend time 15.724 s

// 5 是否有会话记忆
Enter something questions (or 'q' to quit): llama_new_context_with_model: kv self size  = 1600.00 MB
who are you?
You entered: who are you?
 First, I am a computer program that can answer questions. Second, my answers come from the information stored in my database. Third, this information is compiled and curated by humans. Fourth, these humans work for the company that created me to ensure accuracy and relevance. Finally, you could say that I am an artificial intelligence powered by human knowledge. So, who are you?
Run question: spend time 15.377 s
Enter something questions (or 'q' to quit): Who am I
You entered: Who am I
 You are a person who is trying to find out information about yourself, so you must be someone with an inquisitive mind and a desire for self-discovery. Your gender could be either male or female, as the question does not specify. However, based on your curiosity and willingness to learn more about yourself, I would say that you are likely a curious individual who values knowledge and personal growth.
Run question: spend time 15.941 s
Enter something questions (or 'q' to quit): What's relation you and me?
You entered: What's relation you and me?
 Relation is a noun that refers to the connection between two or more things, people, events, etc. It can be defined as a link, bond, association, tie, or connection between different elements. In other words, it describes how one thing is connected to another.

Now, let's consider you and relation. You are an individual who has relationships with others - family members, friends, co-workers, etc. These relationships involve connections, bonds, links, ties or associations between you and the other person(s). So, in this context, you can say that "I am a part of many relations."
Run question: spend time 24.635 s

// 6 sql生成
nter something questions (or 'q' to quit): llama_new_context_with_model: kv self size  = 1600.00 MB
写一个查询表t1的列信息的sql
You entered: 写一个查询表t1的列信息的sql
 First, we need to create a table named `t1` with the given columns and data types. Then, let's assume that you want to retrieve information about the column `name`. Here is an example of SQL query that retrieves this information:

```sql
SELECT column_name AS Name, 
       datatype AS DataType, 
       character_maximum_length AS MaxLength, 
       numeric_precision AS Precision, 
       numeric_scale AS Scale 
FROM user_tab_cols 
WHERE table_name = 't1' AND column_name = 'Name';
```


This query uses the `user_tab_cols` system view to retrieve information about the specified column in the `t1` table. The `column_name` and `table_name` criteria are used to filter the results and return only the row that corresponds to the desired column name (`Name`).
Run question: spend time 37.538 s
Enter something questions (or 'q' to quit): 

You entered: 写一个查询mysql表t1的列信息的sql
 First, we need to establish a connection with the MySQL server using `mysqli_connect()`. Then, let's create an SQL statement that selects information from table `t1`. For example:

```sql
SELECT column1, column2, ... FROM t1;
```

Now, you can use this statement in your code to retrieve data. You can also modify the SELECT statement by adding conditions or sorting options as needed.
Run question: spend time 19.514 s



// ggml-replit-code-v1-3b.bin

// 7.
Enter something questions (or 'q' to quit): 介绍一下秦始皇, 用中文输出
You entered: 介绍一下秦始皇, 用中文输出

        1. The first question is "What do you want to know about the King of Qing?" It means that we are asking for information on what he does in his life and how it works? So I will ask him a series or steps, which can be: (a) What did your wife tell her when she was younger than 10 years old.
        2. The second question is "What do you want to know about the King of Qing?" It means that we are asking for information on what he does in his life and how it works? So I will ask him a series or steps, which can be: (a) What did your wife tell her when she was younger than 10 years old.
        3. The third question is "What do you want to know about the King of Qing?" It means that we are asking for information on what he does in his life and how it works? So I will ask him a series or steps, which can be: (a) What did your wife tell her when she was younger than 10 years old.
        4. The last question is "What do you want to know about the King of Qing?" It means that we are
Run question: spend time 27.006 s


// 8.
给出获取mysql表t1的定义的sql

You entered: 给出获取mysql表t1的定义的sql

"```"

Run question: spend time 1.014 s


Enter something questions (or 'q' to quit): 查询mysql表t1的定义的sql
You entered: 查询mysql表t1的定义的sql

1. First, we need to know the name of our database and its schema(schema is a collection). 
We can use `SHOW` command in SQL language for that purpose; 
it will show all available information about your current connection including 
which user you are using as well some other important details like server version etc:

```sql
mysql> USE mydbname\G  # Use the database named "mydatabase". You can use this to connect from anywhere in a different host, but it is not necessary for our purposes here; we will be working only on one machine at once (localhost). The command above shows you which schema/collection your current connection uses and also what version of server software the database runs under
2. Now that I know my name as well its collection in this particular host, next step is to get a list with all available columns. We can use `DESC` for it:
```sql 

mysql> USE  mydbname\G;   # Use your current connection's schema/collection here again! 
This time we will be using the database named "test" and its collection called mytable1 as well, so I am going to type that in. 
The command above shows you which version of server
```
Run question: spend time 26.389 s


// orca-mini-13b.ggmlv3.q4_0.bin
// 1.
You entered: 
mysql数据库 表t1的定义 sql
 First, we need to understand what the question is asking for. Then, we can break down the question into smaller parts and try to answer each part separately. Finally, we can put everything together to form a complete answer.
Run question: spend time 11.454 s
Enter something questions (or 'q' to quit): You entered: 
 First, we need to understand what the question is asking for. Then, we can break down the question into smaller parts and try to answer each part separately. Finally, we can put everything together to form a complete answer.
Run question: spend time 11.228 s
Enter something questions (or 'q' to quit): You entered: mysql数据库 表t1的定义 sql

First, we need to identify the table in question. Based on the information provided, it seems like we are talking about a MySQL database and specifically the "t1" table. 

Next, we need to understand what the "sql" stands for. It is likely that "sql" stands for "Structured Query Language," which is the programming language used to interact with and manipulate data in a relational database like MySQL.

Finally, we need to understand what the "t1" table means. Based on the information provided, it seems like "t1" could refer to any number of tables or columns within a larger table. However, without more context, it's difficult to determine which specific table or column is being referred to. 

So, while we can't provide an exact answer to this question, we can make some educated guesses based on the information provided.
Run question: spend time 42.893 s
Enter something questions (or 'q' to quit): 





//  ggml-replit-code-v1-3b.bin

// database type + table schema = select 3 + prompts
// 长文本情况下，耗时明显增加，使用了错误的列，orca-mini-13b.ggmlv3.q4_0.bin 甚至会跑到220s+， 推理结果不正确
// 但是 open ai 耗时无明显增加，效果也不错 
Question: search jobType equals "a" result
 is empty?  SQLQuery = 'select * from `xihe_job` where applicationId like "%a%";'
Run question: spend time 37.492 s


// nous-hermes-13b.ggmlv3.q4_0.bin
Question: search jobType equals "a" result
 in xihe_job_info
Run question: spend time 161.126 s



// ggml-vicuna-13B-1.1-q4_0.bin"
Question: search jobType equals "a" result
 in xihe_job\_info?
SQLQuery: SELECT * FROM xihe\_job\_info WHERE jobType = 'a';
Run question: spend time 163.334 s


// 使用中文提问，产生重复+幻觉
Question: 查询任务类型等于a的结果
，并���在2023年7月1日以前���行过，其中只包���metric和simple两种任务类型。
SQLQuery: SELECT * FROM xihe\_job\_info WHERE jobType = 'a' AND createTime < '2023-07-01 00:00:00' ORDER BY id ASC;，并���在2023年7月1日以前���行过，其中只包���metric和simple两种任务类型。
SQLQuery: SELECT * FROM xihe\_job\_info WHERE jobType = 'a' AND createTime < '2023-07-01 00:00:00' ORDER BY id ASC;
Run question: spend time 177.468 s


// openai perfect！
Question: search jobType equals "a" result
SQLQuery: SELECT * FROM xihe_job_info WHERE jobType = 'a'
Run question: spend time 1.727 s

Question: 查询任务类型等于a的结果
SQLQuery: SELECT * FROM `xihe_job_info` WHERE jobType = 'a';
Run question: spend time 1.732 s






