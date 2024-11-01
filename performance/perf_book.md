

# Performance Analysis and Tuning on Modern CPU

[toc]

## 工具 

测量工具 [temci](https://github.com/parttimenerd/temci)

自动化性能回归测试框架
- https://github.com/JoeyHendricks/STATS-PAL
- https://github.com/evergreen-ci/evergreen

 微基准测试工具: 
- C++ [google/benchmark](https://github.com/google/benchmark)
- Julia [BenchmarkTools.jl](https://github.com/JuliaCI/BenchmarkTools.jl)
- Java [JMH](https://github.co(m/openjdk/jmh)
  - openJDK 工具列表 [code-tools](https://openjdk.org/projects/code-tools/)


性能分析工具

- Intel Vtune  
  - for x86
  - AMD [uProf](https://www.amd.com/en/developer/uprof.html)
  -  底层还是 linux perf
- Linux Perf  最广泛使用
  - Flame Graphs 高级分析
  - [KDAB/hotspot](https://github.com/KDAB/hotspot) 用于性能分析的Linux perf GUI
  - [Netflix/flamescope](https://github.com/Netflix/flamescope) FlameScope是一个可视化工具，用于探索不同的时间范围作为火焰图，允许快速分析性能问题，如扰动，方差，单线程执行等。

内存分析工具
- heaptrack KDE开发的用于Linux的开源堆内存分析器
  - `apt install heaptrack-gui`


Continuous profiling 生产环境中监控性能的重要工具

它们通过调用堆栈收集系统范围内的性能指标，持续数天、数周甚至数月。这样的工具可以更容易地发现性能变化的点和问题的根本原因。
- [Parca](https://github.com/parca-dev/par)

### 分析

#### TMA(Top-down Microarchitecture Analysis) 分析
这种分析方法从高层次的角度出发，通过观察程序执行时的微观架构特征，将瓶颈分类为几个主要类别，例如前端绑定（Front End Bound）、后端绑定（Back End Bound）、退休（Retiring）和坏推测（Bad Speculation）。


- 前端绑定（Front End Bound）：这种情况发生在CPU的前端（负责指令预取、解码和分配）成为系统性能瓶颈时。通常表现为指令预取不畅或解码阶段出现问题，导致指令不能有效地送入CPU的执行单元。这可能是由于内存访问延迟、分支预测错误或缓存未命中等原因造成的。

- 后端绑定（Back End Bound）：当CPU的后端（执行单元和退休队列）无法跟上指令流入的速度时，就会出现后端绑定。这通常意味着CPU的执行资源（如ALU、浮点单元等）正在被充分利用，但由于指令依赖、资源争用或内存带宽限制等原因，无法更快地完成指令的执行。

- 退休（Retiring）：退休指的是CPU将完成的指令从执行管线中移出并提交结果给寄存器文件的过程。如果退休过程成为瓶颈，这通常意味着CPU的执行单元正在以最大能力运行，但是由于指令依赖或其他因素，无法持续保持高退休率，导致性能受限。

- 坏推测（Bad Speculation）：这种情况发生在CPU预测分支结果不准确时。现代CPU使用分支预测来提前加载和执行可能需要的指令。如果预测错误，已经投入执行的指令将被废弃，而正确路径的指令需要重新加载和执行，这会导致性能损失。坏推测可能由分支预测器的不准确或复杂的控制流导致。

**什么是无瓶颈**

在理想情况下，一个程序的性能表现应该是均衡的，没有明显的性能瓶颈。然而，在实际应用中，很难达到完全均衡的占比，因为不同类型的任务和工作负载会导致CPU的不同部分（前端、后端、退休和分支预测）以不同的速率运行。

例如，对于计算密集型任务，后端绑定（Back End Bound）的占比可能会更高，因为这类任务需要大量的计算资源。而对于内存密集型任务，前端绑定（Front End Bound）可能会更显著，因为这类任务涉及大量的内存访问，可能导致数据加载成为限制因素。

“退休”和“坏推测”，它们并不是一种常态的性能指标，而是特定条件下影响性能的因素。理想状态下，我们希望尽量减少坏推测带来的性能损失，确保大多数指令都能够顺利退休。


当退休（Retiring）成为瓶颈时，意味着CPU的退休阶段（Retiring stage）无法以足够高的速度完成指令的退休过程，即将指令的计算结果写入寄存器或内存。这通常表现为以下几个方面：

- 低退休率：CPU的退休率是指每周期内完成退休的指令数量。如果退休率低于CPU设计的最大退休能力，这可能表明退休阶段存在瓶颈。

- 高周期活动.STALLS_L3_MISS：这个性能指标表示在L3缓存未命中时，CPU循环活动但因为等待指令退休而发生STALL（停顿）的周期数量。如果这个指标很高，可能意味着退休过程是瓶颈。

- 高比例的Retiring指标：在使用TMA分析时，如果Retiring指标占比较高，这可能表明退休过程是限制程序性能的一个因素。

- 性能受限于指令完成：程序的性能受限于指令完成而非指令发射，即CPU的执行单元在等待已完成计算的指令退休，以便释放资源给新的指令。

- 高指令:周期比：如果程序的指令:周期比（Instructions Per Cycle，IPC）较低，这可能意味着CPU在每个周期内发射的指令数量少，而退休的指令数量也相应减少，导致性能受限。

- 资源利用不均衡：如果CPU的某些执行端口（如浮点单元或整数单元）长时间处于空闲状态，而其他端口则过载，这可能导致退休阶段成为瓶颈，因为完成的指令无法及时退休，从而阻塞后续指令的发射和完成。

解决退休瓶颈的方法可能包括优化代码以减少指令数量、平衡指令发射、减少指令依赖和优化内存访问模式等。此外，还可以通过编译器优化和适当的硬件资源配置来提高退休阶段的效率。


##### 优化

优化前端绑定（Front End Bound）、后端绑定（Back End Bound）、退休（Retiring）和坏推测（Bad Speculation）的问题通常涉及到编译器优化、程序设计和硬件平台的调整。针对每种情况，以下是一些可能的优化策略：

###### 优化前端绑定（Front End Bound）

**策略：**
- **改进代码布局和分支预测**：
   - 减少条件分支指令，特别是那些难以预测的分支。
   - 使用循环展开以降低循环内的分支频率。
   - 利用编译器指令调度和指令级并行度提升，确保指令流连续，减少分支预测失败和相关惩罚。

- **增大指令缓存大小或优化指令预取**：
   - 如果前端绑定源于指令缓存未命中，增加缓存容量或优化预取策略可减少这类问题。

###### 优化后端绑定（Back End Bound）

**策略：**
- **数据局部性优化**：
   - 通过重组循环、利用空间局部性来减少缓存未命中的情况，增强数据预取效果。
   
- **减少数据依赖**：
   - 使用软件流水线技术分解计算阶段，消除不必要的依赖关系。
   - 利用SIMD（单指令多数据流）指令集来同时处理多个数据元素。
   - 利用并行性：通过多线程和向量化指令，充分利用CPU的并行执行能力。
   - 减少指令依赖：通过代码变换技术，如循环展开（Loop Unrolling）和并行化，减少指令之间的依赖。
   - 优化编译器优化选项：使用适当的编译器标志来开启或关闭特定的优化，如内联函数、自动向量化等。

- **提高内存带宽**：
   - 如果瓶颈在于内存访问，可能需要考虑使用更高带宽的内存系统或者优化内存访问模式。

###### 优化退休（Retiring Instructions）

**策略：**
- **减少乱序执行后的冲销**：
   - 避免可能导致乱序执行后无效化指令的操作，如避免过多的内存屏障或锁定指令。
- 提高指令级并行性（ILP）：通过代码重构，增加可以同时退休的指令数量。
- 减少长指令序列：避免编写会导致连续多个简单指令的代码，这些简单指令可能会阻塞退休队列。
- 优化数据结构：使用更紧凑的数据结构和访问模式，减少内存带宽的压力。
   
- **改善分支预测准确性**：
   - 对于关键路径上的分支，优化分支逻辑或使用软件预测 hints。

###### 优化坏推测（Bad Speculation）

**策略：**
- **分支预测优化**：
   - 减少分支：通过代码重排和预测分支的优化，减少分支指令的数量。
   - 使用分支目标缓冲区（BTB）：通过优化BTB的大小和组织结构，提高分支预测的准确性。
   - 避免长序列的推测执行：在代码中插入显式的同步点，以限制错误的推测执行路径的长度。
   - 利用编译器提供的分支预测提示，如 `likely` 和 `unlikely` 标注。

- **减少 Speculative Execution 的风险**：
   - 针对 speculative buffer overflow 类型的安全漏洞（如 Spectre），可以采用防御性编程技术，减少敏感信息泄露的风险。


在实际应用中，优化上述瓶颈不仅需要深入理解程序的行为，还需要对底层硬件有详尽的知识，并结合编译器选项和微架构特性进行细致的调整。对于非常具体的场景，还可能需要针对性地修改处理器微架构或开发专门的编译器优化策略。

#### perf 瓶颈分类
`perf stat --topdown -a -- taskset -c 0 ./benchmark.exe`

perf 工具和 taskset 工具来收集运行名为 ./benchmark.exe 的程序的性能数据，并应用TMA（Top-Down Microarchitecture Analysis）分析来识别性能瓶颈。

各个部分解释如下：

perf stat: 这是 perf 工具的一个子命令，用于统计和报告程序运行时的性能事件。
--topdown: 这个选项指示 perf 启用TMA分析，它会收集CPU性能事件并尝试确定程序的性能瓶颈。
-a: 这个选项告诉 perf 收集整个系统的性能数据，而不仅仅是特定进程的数据。
--taskset -c 0: 这是 taskset 命令的参数，用于将执行的进程绑定到CPU核心0上。这样可以确保性能分析的目标程序在特定的CPU核心上运行，排除其他核心上的活动对性能数据的影响。
./benchmark.exe: 这是要分析的程序的名称，它应该在当前工作目录下可执行。

并收集整个系统的性能数据，同时将该程序绑定到CPU核心0上执行，以便进行TMA分析，从而识别可能存在的性能瓶颈。

由于我们已经使用taskset -c 0将基准测试固定到核心0，因此我们只需要关注与S 0-C 0对应的行。我们可以丢弃其他行，因为它们正在运行其他任务或保持空闲。

Linux perf只支持1级TMA指标，因此要访问2级、3级TMA指标，我们将使用由Andi Kleen编写的[pmu-tools](https://github.com/andikleen/pmu-tools)中的toplev工具

```
$ ~/pmu-tools/toplev.py --core S0-C0 -l3 -v --no-desc taskset -c 0 ./benchmark.exe
...
# Level 1
S0-C0 Frontend_Bound: 13.91 % Slots
S0-C0 Bad_Speculation: 0.24 % Slots
S0-C0 Backend_Bound: 53.36 % Slots <==
S0-C0 Retiring: 32.41 % Slots
# Level 2
S0-C0 FE_Bound.FE_Latency: 12.10 % Slots
S0-C0 FE_Bound.FE_Bandwidth: 1.85 % Slots
S0-C0 BE_Bound.Memory_Bound: 44.58 % Slots <==
S0-C0 BE_Bound.Core_Bound: 8.78 % Slots
# Level 3
S0-C0-T0 BE_Bound.Mem_Bound.L1_Bound: 4.39 % Stalls
S0-C0-T0 BE_Bound.Mem_Bound.L2_Bound: 2.42 % Stalls
S0-C0-T0 BE_Bound.Mem_Bound.L3_Bound: 5.75 % Stalls
S0-C0-T0 BE_Bound.Mem_Bound.DRAM_Bound: 47.11 % Stalls <==
S0-C0-T0 BE_Bound.Mem_Bound.Store_Bound: 0.69 % Stalls
S0-C0-T0 BE_Bound.Core_Bound.Divider: 8.56 % Clocks
S0-C0-T0 BE_Bound.Core_Bound.Ports_Util: 11.31 % Clocks
```

将进程固定到CPU 0（使用taskset -c 0），并将toplev的输出限制为仅此核心（--core S 0-C 0）。选项-l2告诉工具收集Level 2指标。选项--no-desc禁用每个度量的描述。

应用程序的性能受到内存访问的限制（Backend_Bound.Memory_Bound）。几乎一半的CPU执行资源都浪费在等待内存请求完成上。

我们发现瓶颈在DRAM_Bound中。这告诉我们，许多内存访问在所有级别的缓存中都未命中，并一直到主存。如果我们收集程序的L3缓存未命中的绝对数量，我们也可以确认这一点。


#### 在代码中找到位置

作为TMA过程中的第二步，我们在代码中定位所识别的性能事件最频繁发生的位置。为此，应该使用与步骤1中确定的瓶颈类型相对应的事件对工作负载进行采样.

使用--show-sample选项运行toplev工具

为了找到导致DRAM_Bound指标如此高的值（L3缓存中的未命中）的内存访问，我们应该对MEM_LOAD_RETIRED.L3_MISS_PS精确事件进行采样。

`perf record -e cpu/event=0xd1,umask=0x20,name=MEM_LOAD_RETIRED.L3_MISS/ppp ./benchmark.exe`

```
perf report -n --stdio
...
# Samples: 33K of event ‘MEM_LOAD_RETIRED.’L3_MISS
# Event count (approx.): 71363893
# Overhead Samples Shared Object Symbol
# ........ ......... .............. .................
#
99.95% 33811 benchmark.exe [.] foo
0.03% 52 [kernel] [k] get_page_from_freelist
0.01% 3 [kernel] [k] free_pages_prepare
0.00% 1 [kernel] [k] free_pcppages_bulk
```

几乎所有的L3未命中都是由可执行benchmark.exe中函数foo的内存访问引起的。

示例程序，分配了一个足够大的数组a，使其无法容纳6 MB的L3缓存。基准测试生成一个随机索引到数组a中，并将该索引与数组a的地址一起沿着给foo函数。稍后，foo函数读取这个随机内存位置。

```
int main() {
char* a = (char*)malloc(_200MB); // 200 MB buffer
...
for (int i = 0; i < 100000000; i++) {
int random_int = distribution(generator);
// 优化
+ __builtin_prefetch ( a + random_int, 0, 1);
foo(a, random_int);
}
...
}
```

### 分支预测失败


## 源码优化

软件优化
- 系统优化。分析程序中使用的算法和数据结构，看看你是否能找到更好的。示例：使用快速排序而不是冒泡排序。
- 简化计算。
  - 如果一个算法是高度并行化的，那么让程序多线程化，或者考虑在GPU上运行它。目标是同时做多件事。
  - 并发已经在硬件和软件堆栈的所有层中使用。示例如下：将工作分布在多个线程上;在数据中心的多台服务器之间平衡负载;在等待IO操作时使用TCP/IP IO以避免阻塞;保持多个并发网络连接以重叠请求延迟。
- 消除冗余工作。不要做你不需要或已经做过的工作。示例如下：利用更多的RAM来减少你必须使用的CPU和IO的数量（缓存，查找表，压缩）;预先计算编译时已知的值;将循环不变式计算移动到循环之外;通过引用传递C++对象以消除通过值传递引起的过多副本。
- 分批。聚合多个类似的操作并一次性完成，从而减少多次重复操作的开销。示例如下：发送大的TCP数据包，而不是许多小的数据包;分配一大块内存，而不是为数百个小对象分配空间。
- 排序。重新排列算法中的操作序列。示例如下：更改数据布局以启用顺序内存访问;根据类型对C++多态对象数组进行排序，以更好地预测虚函数调用;将热函数分组在一起，并将它们放在二进制文件中彼此更接近。

其他
- 用另一种语言重写代码：如果程序是使用解释型语言（Python，JavaScript等）编写的，用开销较小的语言重写其性能关键部分，例如，C++、Rust、Go等。
- 优化编译器选项：检查你是否至少使用了这三个编译器标志：-O3（启用与机器无关的优化），-march（启用针对特定CPU架构的优化），-flto（启用过程间优化）。
- 优化第三方软件包：绝大多数软件项目都利用专有和开源代码层。这包括操作系统、库和框架。您可以通过替换、修改或重新配置其中一个部分来寻求改进。
- 购买更快的硬件，例如，一旦发现内存带宽限制了多线程程序的性能，您可能会建议购买具有更多内存通道和DIMM插槽的服务器主板和处理器。


### 优化内存访问-TMA：MemoryBound类别
- 数据对齐和填充：确保数据结构对齐，以利用CPU缓存的效率，避免虚假共享。
- 数据局部性优化：
尽量让相关的数据在一起，利用缓存行填充（cache line padding）避免伪共享（false sharing）。
- 使用数组而不是单独的变量，使得数据能更好地利用缓存。
矩阵转置、循环展开等技术，提升空间局部性。
- 预取（Prefetching）：
利用硬件预取指令提前将即将使用的数据载入高速缓存。
编译器或手动插入预取指令，对于连续访问的大块数据尤其有效。
- 减少内存分配和释放：
适当合并内存分配，减少内存碎片，提高内存管理效率。

### 优化计算-TMA：CoreBound类别
- 指令级并行（ILP）：
利用SIMD（Single Instruction Multiple Data）指令集进行向量化计算。
利用编译器自动向量化或者手动编写SIMD代码。
- 循环展开：增加循环的迭代次数，减少循环开销，提高指令级并行性。
- 多线程并行计算：
分解计算任务，合理利用多核CPU资源，通过OpenMP、Pthreads等库创建并行区域。
- 利用FPGA或GPU加速：
对于计算密集型任务，考虑使用GPU进行并行计算，或针对特定硬件定制的FPGA实现加速。

### 优化分支预测-TMA：BadSpeculation类别

- 简化分支结构：
避免过于复杂的分支逻辑，尤其是条件分支深度过深或者分支分布不均匀的情况。
- 使用分支预测提示：
在编译器支持的情况下，为分支指令添加likely或unlikely提示，帮助编译器生成更准确的分支预测代码。
- 循环展开和软件流水线：
将循环体展开以减少分支跳转，同时注意保持良好的数据局部性。
- 避免长序列的推测执行：在代码中插入显式的同步点，限制错误的推测执行路径的长度。
### 机器代码布局优化-TMA：FrontEndBound类别

- 指令调度（Instruction Scheduling）：
使用高级编译器的指令调度优化，使机器码指令流更加有序和连续。
- 函数内联（Function Inlining）：
针对小型、频繁调用的函数，可以考虑内联以减少函数调用开销和提高指令缓存利用率。将热点函数内联到它们的调用者中。
- 循环展开与重组：
将循环展开以减少控制流指令，提高指令缓存的效率。


### 优化多线程程序

- 工作负载均衡：
动态负载分配，确保各线程间的负载大致均衡，避免某些线程空闲而其他线程过载。
- 线程局部存储：使用线程局部变量来减少线程间的数据竞争。
- 避免上下文切换：通过合理的线程管理和内存布局减少线程上下文切换的开销。
- 锁优化：
减少锁竞争，使用无锁数据结构或原子操作替代互斥锁。
- 细粒度并行（Task-based parallelism）：
使用C++的std::async、std::future或者第三方库如Intel TBB等实现细粒度并行任务划分。
- 同步原语选择：
根据实际应用场景选择合适的同步机制，如自旋锁、条件变量等。




## REF
- [github: perf-book](https://github.com/dendibakh/perf-book)
    - tex 文本，如果是Ubuntu 22.04系统，miktex 似乎还是无法工作（遇到`qt.qpa.plugin: Could not find the Qt platform plugin "xcb" in "/usr/lib/x86_64-linux-gnu/qt5/plugins"`），建议 执行 python export_book.py 之后，生产book.tex之后，使用 texmaker 打开 book.tex 文件， 构建，打印出 pdf
    ```
    # 安装完全版 latex 软件 texlive
    sudo apt-get install texlive-full
    # 安装可视化工具 texmaker
    sudo apt-get install texmaker
    ```
 
- [[论文阅读] A Top-Down Method for Performance Analysis](https://www.bluepuni.com/archives/paper-reading-a-top-down-method-for-performance-analysis/) Intel (amd cpu似乎不支持)