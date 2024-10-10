## 日志异常检测Log Anomaly Detection

### 应用场景

京东科技全链路故障：

- 目的：运维日志模版提取，及时捕捉线上未知的业务异常问题

- 应用日志反应应用本身运行状态，某些故障是能够从监控指标上发现的，然后由于部分监控指标的缺失，有些故
障的产生并不能从指标层面发现，需要从日志中发现问题并定位根因。

- 通过智能提取日志模版技术对历史全量日志聚类，在线实时匹配发现已知类问题的日志量变化，并可及时捕捉到
新的日志模式，从日志角度提升监控能力。（关键日志模式数量告警）


### drain 模式识别算法

日志解析结果：

![](log_images/image1.png)

日志解析数据结构：

![](log_images/image2.png)

日志解析过程更新：

![](log_images/image3.png)

处理步骤：

1. 预处理，领域知识正则匹配。DRAIN允许用户基于表示常用变量(如IP地址和块ID)的域知识提供简单的正则表达式。然后，DRAIN将从原始日志消息中删除与这些正则表达式匹配的token。（删除或者用*替换？）

2. 第一层处理，解析树中的第一层节点表示日志消息具有不同日志消息长度的日志组。对于日志消息长度，我们指的是日志消息中的token数。在此步骤中，DRAIN基于经预处理的日志消息的日志消息长度来选择到第一层节点的路径。
   
   1. 基于具有相同日志事件的日志消息可能具有相同的日志消息长度的假设。尽管具有相同日志事件的日志消息可能具有不同的日志消息长度，但可以通过简单的后处理进行处理。此外，我们在第四-B节中的实验证明了即使在没有后处理的情况下，DRAIN在分析准确率方面也具有优势。

3. 在此步骤中，DRAIN从在步骤2中搜索的第1层节点遍历到叶节点。
   
   1. 此步骤基于这样的假设，即日志消息开始位置中的token更可能是常量。
   
   2. 具体地说，DRAIN根据日志消息开始位置中的标记选择下一个内部节点。
   
   3. 在这一步中，DRAIN遍历的内部节点数为(Depth−2)，其中Depth是限制所有叶节点的深度的解析树参数。因此，存在将日志消息中的第一个(Depth−2)token编码为搜索规则的(Depth−2)层。
   
   4. 为了避免分支爆炸，我们在此步骤中只考虑不包含数字的token。如果token包含数字，它将匹配特殊的内部节点“*”。
   
   5. 定义了一个参数MaxChild，它限制了节点的最大子节点数。如果某个节点已经有了MaxChild子节点，则任何不匹配的token都将在其所有子节点中匹配特殊的内部节点“*”。
   
   6. 例如，对于日志消息“从节点4接收”，排出从第一层节点“长度：4”遍历到第二层节点“接收”，因为在日志消息的第一个位置的token是“接收”。

4. 然后DRAIN将遍历到与内部节点RECEIVE链接的叶节点，并转到步骤4。
   
   1. 在此步骤之前，DRAIN已遍历到包含日志组列表的叶节点。这些日志组中的日志消息遵循路径沿线的内部节点中编码的规则。
   
   2. 在此步骤中，DRAIN从日志组列表中选择最合适的日志组。我们计算每个日志组的日志消息和日志事件之间的相似度simSeq。

5. **更新解析树**
   
   1. 如果在步骤4中返回合适的日志组，则DRAIN会将当前日志消息的日志ID添加到返回的日志组中的日志ID中。此外，还会更新返回日志组中的日志事件。
   
   2. 具体而言，DRAIN扫描位于日志消息和日志事件相同位置的token。
   
   3. **如果两个token相同，则不会修改该位置中的token。否则，我们通过日志事件中的通配符(即*)来更新该位置中的token。（&计算，相同保留，不同设置为*）**
   
   4. 如果DRAIN找不到合适的日志组，它将根据当前日志消息创建一个新的日志组，其中日志ID仅包含日志消息的ID，而日志事件正是日志消息。
   
   5. 然后，DRAIN将使用新的日志组更新解析树。

### ULP (An Effective Approach for Parsing Large Log Files)

非流式算法，只能用于离线方式的聚类



ULP利用这样idea，即如果我们对属于同一组的日志事件实例而不是整个日志文件本地使用频率分析，则可以更好地识别日志事件的静态和动态令牌。

该方法通过字符串匹配相似度建立相似的日志事件组，并对同一组实例进行局部频率分析来区分静态和动态令牌，从而区分静态和动态令牌。

我们的技术的平均准确率为89.2%，而次佳的排水法的平均准确率为73.7%。此外，ULP可以在3分钟内解析包含多达400万个日志事件的大文件。

对相似的日志事件进行预处理、分组，并使用局部频率分析生成日志模板。

- 第一步是预处理步骤，其中标识诸如时间戳、日志级别和日志记录功能之类的报头。我们还根据常见的正则表达式检测不重要的动态令牌，如IP和MAC地址。

- ULP的第二步是识别相似的日志事件并将它们分组在一起。为此，我们使用文本相似性度量。

- 一旦形成了相似的日志事件组，我们就对每个组的实例进行频率分析，以确定静态和动态token，并导出各种日志模板，然后将这些模板映射回每个日志事件。算法1显示了ULP的步骤。

- 将发生频率低于最大频率的任何事情视为动态token。



在某些方面，我们的方法在原则上更接近AEL的方法。可以使用AEL方法基于语言共性对日志事件进行分类。然而，从简单的动态模式开始，AEL使用基于系统信息(例如，IP地址、编号和存储位置)的硬编码算法来识别更复杂的模式。然后，生成的日志事件被标记化，并根据它们包含的字数入库。在将日志消息抽象为模板以供系统中其他地方使用之前，该分类会评估每个bin中的日志消息。

AEL的困难在于，它假设具有相同字数的事件属于同一组，从而导致在分析日志事件时出现许多误报。ULP利用字符串匹配相似性，将静态token和日志事件中的token数量相结合，以克服这一问题。

DRAIN的作者做出的另一个假设是，长度相似的日志事件属于同一组，而不必检查事件的内容，这会导致将非常不同的日志事件归入同一组。ULP通过应用严格的字符串匹配技术来克服这一问题，以确保只有当日志事件共享相同的静态token时，才能将它们分组在一起。（批评的不合理？长度只是初步分组，还有前缀字符是否一致）

至于Logram，它的主要限制之一在于它处理只出现一次的日志事件的方式。对于这些事件，Logram认为整个日志模板仅由动态变量组成。LOGRAM的另一个限制与n元语法的使用有关，这导致如果n元语法序列不像其他序列那样频繁出现，则它们可以被视为动态变量的情况。

For example, in the log event "Resolved 04DN8IQ.fareast.corp.microsoft.com to /default-rack", the 2-gram "Resolved 04DN8IQ.fareast.corp.microsoft.com" appears only twice in the log file as opposed to the 2-gram "to /default-rack" which appears more frequently, the template generated for this log event is "<*> <*> to /default-rack", which is not valid ("Revolved"should be detected as a static token).

优点：

与其他日志解析器不同，ULP不假设静态或动态令牌的位置。例如，DRAIN假定出现在日志消息开头的令牌是静态令牌，这并不总是有效的。

此外，ULP能够从各种未知日志文件中检测动态令牌和日志模板，而无需在预处理阶段使用领域知识正则表达式，例如对于DRAIN[26]和Logram[27]的情况。ULP仅利用泛型正则表达式。

缺点：

如果同一动态令牌的重复次数与静态令牌相同，则ULP将对其进行错误分类。解决这一问题的一种方法是通过针对这些变量来改进预处理步骤。



**优点：**

- **速度快**
- **无调参**

**缺点：**

- **offline**



### Logram

基本原理：

- 基于日志生成 3-grams，2-grams 字典

- 对字典根据设置阈值，阈值根据automated approach （自动化，但是代码中是直接给出的各个测试集的3，2元语法阈值），对日志划分为静态和动态索引

- 先检查3元，然后检测2元

- 对非静态，常量token，使用<*>代替

Logram 使用字典来存储日志中 n-grams 的频率，并利用 n-gram 字典来提取日志中的静态模板和动态变量。我们的直觉是，频繁的 n-grams 更可能代表静态模板，而罕见的 n-grams 更可能是动态变量。n-gram 字典可以有效地构建和查询，即复杂度分别为 O(n) 和 O(1)。



支持在线解析，因为当不断添加更多日志时(例如，在日志流场景中)，可以高效地更新n元语法词典。在我们的Logram在线实施中，我们以流的方式馈送日志(即每次馈送一条日志消息)。当读取第一条日志消息时，词典为空(即，所有n元语法都为零)，因此Logram将所有令牌解析为动态变量。然后，Logram使用从第一个日志消息中提取的n元语法创建词典。在此之后，当读取随后的每个日志消息时，Logram使用现有的ngram词典来解析日志消息。



**缺点：**

- **准确性未到达论文声称的水平，调n-gram阈值参数很影响结果，但是未给出具体自动化方法**
- **词典构建空间开销，online模式，初始部分日志，模板全处理成<*>**



## REF

- [面向跨语言的操作系统日志异常检测技术研究与实现-51CTO.COM](https://www.51cto.com/article/714875.html)

- https://github.com/AICoE/log-anomaly-detector

- drain:
  
  - [GitHub - logpai/Drain3: Drain log template miner in Python3](https://github.com/logpai/Drain3)
  
  - [Drain算法：日志解析_就叫昵称吧的博客-CSDN博客_drain算法](https://blog.csdn.net/qq_39378221/article/details/121212682)
  
  - [知乎-日志解析算法总结](https://zhuanlan.zhihu.com/p/448098972) （drain + spell）

- logpai
  
  - https://github.com/logpai/awesome-log-analysis
  
  - https://github.com/logpai/loglizer
  
  - [GitHub - logpai/logparser: A toolkit for automated log parsing](https://github.com/logpai/logparser)
    
    - [benchmark](https://github.com/logpai/logparser/blob/master/docs/benchmark.rst) 日志解析器准确度基准
    - [GitHub - tianjiqx/logparser: A toolkit for automated log parsing ](https://github.com/tianjiqx/logparser) （python3 调整）



- [快速了解日志概貌，详细解读13种日志模式解析算法 - 云智慧技术社区 - OSCHINA - 中文开源技术交流社区](https://my.oschina.net/yunzhihui/blog/5514043)

- 来自logpai 论文 Tools and Benchmarks for Automated Log Parsing

- [日志自动分析和解析开源工具_logpai_lovelife110的博客-CSDN博客](https://blog.csdn.net/qq_33873431/article/details/103600782)
  
  - 目前，在所研究的 13 个日志解析器中，Drain 的性能最好。该方法不仅平均精度最高，而且方差最小。
  
  - 与其他日志解析器相比，Drain 实现了相对稳定的精度，并且在改变日志量时表现出了鲁棒性。
  
  - Drain 和 IPLoM 具有较好的效率，随日志大小线性增长。
  
  - 当日志数据简单且事件模板数量有限时，日志解析通常是一个有效的过程。例如，HDFS 日志只包含 30 个事件模板，因此所有的日志解析器都可以在一个小时内处理 1GB 的数据。但是，对于具有大量事件模板 (例如，Android) 的日志，解析过程会变得很慢。

- https://pdfs.semanticscholar.org/b35c/38c6f4194e1b0617fc96899e7b4f6f2c846f.pdf logpai slides

- [LogCluster算法_张欣-男的博客-CSDN博客](https://blog.csdn.net/sdlypyzq/article/details/123880720)

- [日志解析LogMine方法 - 简书](https://www.jianshu.com/p/c59570aacb94)

- [**ACM Computing Survey**] [A Survey on Automated Log Analysis for Reliability Engineering](https://arxiv.org/abs/2009.07237)  
  [ACM Computing Survey] 可靠性工程自动化日志分析调查 (推荐)

- Tools and Benchmarks for Automated Log Parsing

- [**IST'20**] [A Systematic Literature Review on Automated Log Abstraction Techniques](https://www.sciencedirect.com/science/article/pii/S0950584920300264)  
  
  - [IST'20] 自动日志抽象技术的系统文献综述



- https://github.com/BlueLionLogram/Logram
  
  - [GitHub - tianjiqx/Logram: Efficient Log Parsing Using n-Gram Dictionaries](https://github.com/tianjiqx/Logram)  支持logpai的基准测试

- https://zenodo.org/record/6425919#.ZEE8L-xBz0p ULP 


- [Paper Notes (log based amomaly detection)日志异常检测 - gaiusyu的文章 - 知乎](https://zhuanlan.zhihu.com/p/522895226)

- [分布式转型时期，日志分析难题如何应对？](https://dbaplus.cn/news-134-5991-1.html) 
  - 基于文本聚类和RNN循环神经网络模型算法，对日志进行智能分类


- Landauer, M., Skopik, F., & Wurzenberger, M. (2023): A Critical Review of Common Log Data Sets Used for Evaluation of Sequence-based Anomaly Detection Techniques. [arxiv:2309.02854](https://arxiv.org/pdf/2309.02854).   基于事件序列的日志异常检测方法review + 日志测试集