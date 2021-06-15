# LeetCode-笔记

[TOC]

解题办法：

抓住题目特征，匹配解题思想，根据解题思想进行建模，考虑细节，实现，用例测试，边界测试。



## 1.  二分查找

```java
public int search (int key, int[] array) {
    int l = 0, h = array.length - 1;
    while( l <= h) {
        int mid = l + (h-l) / 2;
        if (key  == array[mid]) return mid;
        if (key < array[mid]) h = mid -1;
        else l= mid + 1;
    }
    return -1;
}
```

该二分查找的写法，关键：

- 循环条件 l <= h，而不是l < h
- 中值更新mid = l + (h-l)/2
  - 不直接(l+h)/2，避免溢出
- 边界值更新l=mid+1, h = mid -1;（循环l和h可以等，则边界更新时使用开区间）
  - h的更新是由循环条件决定，l <= h时,若h = mid，会导致循环无法退出，如l=1, h=1时，此时mid=1。
  - l<h，若 h =mid -1, 会跳过查找的数，如[1,2,3]，查找1时，l,h.mid，将会是{0,2,1}，{0,0,-} 由于l == h 直接退出循环
  - l<h作为二分查找，是在题目需要检查循环体外l==h结果是否符合预期，例如序列[1,2,3],查询3时，[l,h]为[2,2]跳出循环体，需要检查跳过pos=2的结果是否为查找值。而对于某些题目，就是希望得出区间为1的结果，不是查找mid值，通常使用该循环条件。

二分查找原理(循环条件l<=h)：

给定区间[l,h]，查看中值，比较，迭代选择左，右区间。迭代到最后，l,h有以下几种情形：

- 区间length=4，[l,h]为[0,3]，mid等于1，产生区间长度为1和2的[l,h]子区间
- 区间length=3，[l,h]为[0,2],mid等于1，产生2个区间长度为1的[l,h]子区间
- 区间length=2, [l,h]为[0,1],mid等于0，要么找到退出，要么产生1个区间长度为1的[l,h]子区间
- 区间length=1, [l,h]为[0,0],mid等于0，要么找到，要不未找到，都退出。

二分查找原理2(循环条件l<h)：

给定区间[l,h]，查看中值，比较，迭代选择左，右区间。迭代到最后，l,h有以下几种情形：

- 区间length=4，[l,h]为[0,3]，mid等于1，产生区间2个长度为2的[l,h]子区间[0,1]和[2,3]
- 区间length=3，[l,h]为[0,2],mid等于1，产生区间长度为2和1的[l,h]子区间[0,1]和[2,2]（退出循环，检查是否找到）
- 区间length=2, [l,h]为[0,1],mid等于0，要么找[0,0]到退出，要么找不到也退出循环产生区间[1,1]（注意若循环结束结果，最后需要判断l是否等于查找值）
- 区间length=1, [l,h]为[0,0],mid等于0，该情况是需要在循环体外判断的，循环条件l<h会导致这个结果不会被检查。



二分搜索的变种写法：

- 查找第一个与目标相等的元素
- 查找最后一个与目标相等的元素
- 查找第一个大于等于目标的元素
- 查找最后一个小于等于目标的元素

```java
//1.查找第一个与目标相等的元素
public int searchFirstEqualElement(int[] nums, target int) {
    int l =0, h = nums.length -1;
    while (l <= h){
        int mid = l + (h-l) / 2;
        if (nums[mid] > target) {
            h = mid -1;
        } else if (nums[mid] < target) {
            l= mid +1;
        } else {
            // 找到第一个与target相等的元素
            if (mid == 0 || nums[mid-1] != target){
                return mid;
            }
            h = mid -1;
        }
    }
}
// 2.查找最后一个与目标相等的元素
public int searchLastEqualElement(int[] nums, target int) {
    int l =0, h = nums.length -1;
    while (l <= h){
        int mid = l + (h-l) / 2;
        if (nums[mid] > target) {
            h = mid -1;
        } else if (nums[mid] < target) {
            l= mid +1;
        } else {
            // 找到最后一个与target相等的元素
            if (mid == nums.length -1|| nums[mid+1] != target){
                return mid;
            }
            l = mid + 1;
        }
    }
}
// 3.查找第一个大于等于目标的元素
public int searchFirstGreaterOrEqualElement(int[] nums, target int) {
    int l =0, h = nums.length -1;
    while (l <= h){
        int mid = l + (h-l) / 2;
        if (nums[mid] > target) {
             // 找到第一个大于等于target的元素
            if (mid == 0 || nums[mid-1] < target){
                return mid;
            }
            h = mid -1;
        } else {
            l= mid +1;
        }
    }
}
// 4.查找最后一个小于等于目标的元素
public int searchLastLessOrEqualElement(int[] nums, target int) {
    int l =0, h = nums.length -1;
    while (l <= h){
        int mid = l + (h-l) / 2;
        if (nums[mid] < target) {
             // 找到最后一个小于等于target的元素
            if (mid == nums.length -1|| nums[mid+1] > target){
                return mid;
            }
            l = mid + 1;
        } else {
            h = mid -1;
        }
    }
}
```

适用题型：

- 迭代，数学X^2相关表达式，如求开方sqrt(n)，在0-n之间二分查找mid，mid^2 =n
  - X^2相关表达式变种，如n=(x+1)*x/2,求x，也可以二分查找。判断n=mid * （mid+1）/2。
- 双数组问题
  - LeetCode4 2数组的中间值
  - LeetCode540 有序数组，只有一个数不出现2次，找到这个数
  - LeetCode162 随机数组，返回任意峰值

```java
// l540:解题思想，单数的对象一定在奇数个的有序区间，迭代查询奇数个的区间
// 判断，单值在哪个区间，若mid为偶数位置，左区间是偶数个，右区间也是偶数个。若m与m+1相等，那么m需要加到右边（迭代时，可以直接去掉m和m+1的值），则说明单值在右区间，否则将mid加到左区间，检查左区间。
// 迭代到最后，区间长度为1时退出，即为所需要的单值。
public int singleNonDuplicate(int[] nums) {
    int l =0, h = nums.lengt -1;
    while(l < h) {
        int m = l + (h-l) / 2;
        // 保证l,h,m都是偶数，使查找区间一直是奇数
        if (m % 2 == 1) m--;
        if (nums[m] == nums[m+1]) l= m+2;
        else h = m;
    }
    return nums[l];
}
// l162:解题思想，将数组视为多段交替连续的有序数组，将mid与右表值比较，大于，说明在下降，峰值在左边，小于说明上升，峰值在右表，迭代缩减区间，只剩1个时，即为峰值
public int findPeakElement(int nums) {
    int l =0, h = nums.lengt -1;
    while(l < h) {
        int m = l + (h-l) / 2;
        if (nums[m] > nums[m+1]) h = m;
        else l = mid +1;
    }
    return nums[l];
}

```



## 2. 动态规划

多阶段决策过程，每步处理一个子问题，求解**组合优化问题**

解决递归问题的步骤：

- 定义子问题（问题降阶、增加限制、组合子问题）
- 写递推表达式
  - 递推的表达式未必一定要是最终结果，也可以是限制条件下的初步结果，然后通过max，min求取最终结果
- 识别和处理最基础子问题问题

3特性：

- 最优子结构：最优解所包含的的子问题的解也是最优的，或者所，子问题的最优解，可以推出整个问题的最优解
- 子问题重叠：使用递归，自顶向下对问题求解时，每次的子问题不是新问题，子问题会重复计算多次，将子问题结果保存，获得高效率。
- 无后效性：每个状态都是过去历史的完整总结，以前的各个阶段的状态不影响。





### 1维动态规划

问题：给定n，找出由1，3,4的的组合数量。例如：

n=5, 组合数量时6,

1+1+1+1+1+1

1+1+3

1+3+1

3+1+1

1+4

4+1

定义子问题：Dn表示由1,3,4组成n的组合数量。

递推表达式：Dn=D(n-1)+D(n-3)+D(n-4)

基础情况：D0 = 1;Dn =0 （n<0;

D0=D1=D2=1,D3=2

```java
// 代码
// 改问题与斐波那契问题的变种，都一样，只需要有一次循环，递推到所求结果
D[0]=D[1]=D[2]=1;
D[3]=2;
for (i=4;i<=n;i++)
    D[i]=D[i-1]+D[i-3]+D[i-4];


/* 
POJ2663 Tri Tiling 完美覆盖
现在给出一个3*n（0<=n<=30）的矩阵，要求用1*2的骨牌来填充，问有多少种填充方式？

3*n 需要被2整除，那么n一定非奇数，所以，子问题 可能是f(n-2),f(n-4),f(n-6),f(n-8)... 这类
将n作为列数，n=2时，可以有3个1*2方块组成三种图形。


n=4列，无法被分拆成2列构成的图形（单独2列会截断骨牌），只有2种，n=6，8...列也是一种。
具体图形是分别是（倒）凹型，中间横放骨牌
因此递推
f(0)=1,
f(2)=3,
f(4)=3*f(2)+2*(f(0))
...
f(n-2)=3*(f(n-4))+2(f(n-6)+....f(0))
f(n)=3*f(n-2)+2*(f(n-4)+f(n-6)+....+f(2)+f(0))
f(n)=f(n-2)可得：
f(n)=4f(n-2)-f(n-4)
*/

f[0]=1,f[2]=3;
for(i=4;i<=30;i+=2)
    f[i]=4f[i-2]+f[4];

/*
剑指offer42/leetcode53:
输入一个整型数组，数组中的一个或连续多个整数组成一个子数组。求所有子数组的和的最大值。
要求时间复杂度为O(n)。
分析：
根据连续数组条件，dp[i]设为以i结尾的最大子序列，保证递推式符合连续子序列限制。
递推式：
dp[i]=max(dp[i-1],nums[i])
结果，非一般地，dp[n-1]是结果，而是需要求max(dp[i])
代码见 斐波那契专题，使用了两个max。
*/

/*
leetcode121:股票买卖的最佳时间
给定一个数组 prices ，它的第 i 个元素 prices[i] 表示一支给定股票第 i 天的价格。
你只能选择 某一天 买入这只股票，并选择在 未来的某一个不同的日子 卖出该股票。设计一个算法来计算你所能获取的最大利润。
返回你可以从这笔交易中获取的最大利润。如果你不能获取任何利润，返回 0 。
分析：
最大利润，需要低买高卖。
设dp[i]为以第i天卖出的最大利润(当天价格减去i-1天前最低点价格)。
取max(dp[i])即为所求。
*/
public int maxProfit(int[] prices) {
    int len = prices.length;
    // i天前，买入最低点
    int minPrice = prices[0];
    int maxProfit = 0;
    for (int i=1;i<len;i++){
        maxProfit = Math.max(maxProfit, prices[i]- minPrice);
        // 更新最小值
        minPrice=Math.min(minPrice,prices[i]);
    }
    return maxProfit;
}
```

### 2维动态规划（LCS问题）

```java
/*
leetcode1143:
LCS：
给定2个字符串x，y，找到共同最长公共子序列，并打印长度
例子：
x:ABCBDAB
y:BDCABC
"BCAB"是最长子序列，子序列可以不连续。
那么一个字符串可能的子序列就有2^n个,直接暴力枚举，匹配的开销是2^(m+n)。

分析：
1)定义问题：
因为有2个字符串，所以问题有两个变量，这就是被叫做2维动态规划问题原因。
正如一维动态规划削减问题规模大小，可以分别对2个维度加以限制，降阶问题。
因此，定义问题D[i][j]是以字符串是i,j结束的最长公共子序列。
2)然后用子问题，递推后续的结果的递推公式是：
情形1，Xi=yi,则D[i][j]=D[i-1][j-1]+1
情形2，Xi!=yi,则D[i][j]=max(D[i][j-1],D[i-1][j])
3)最后，初始情形
D[i][0]=D[0][j]=0
*/
// 注意是<=,而不能是<
// 另外，这两个循环也可以放到DP中，但是需要额外判断，提取出来，减少判断，更加清晰，对应初始化
for(i=0;i<=n;i++) D[i][0]=0;
for(j=0;j<=m;j++) D[0][j]=0;

for(i=1;i<=n;i++){
    for(j=1;j<=m;j++){
        // 注意起始从1开始，所以下标需要是-1
        if (x[i-1]==y[j-1]) {
            //D[i-1][j-1] 在上次i-1循环已经求出
            D[i][j]=D[i-1][j-1]+1;
        }else {
            //D[i-1][j] 在上次i-1循环已经求出，D[i][j-1]本内层循环的前一次求出
            D[i][j]=Math.max(D[i-1][j],D[i][j-1])
        }
    }
}
return D[n][m];
// 空间
/*
递推公式，D[i][j]只与前一个D[i][j-1]和上一行的D[i-1][j-1]、D[i-1][j]有关。
所以可以复用数组,最容易理解的是（一维滚动数组）O(m)。
使用2*(m+1)的滚动数组：
*/
int cur,pre;
int D[2][m+1];
for(i=1;i<=n;i++){
    cur = i%2;//当前行
    pre = 1 - now;//上一行
    for(j=1;j<=m;j++){
        if (x[i-1]==y[j-1]) {
            //D[i-1][j-1] 在上次i-1循环已经求出
            D[cur][j]=D[pre][j-1]+1;
        }else {
            //D[i-1][j] 在上次i-1循环已经求出，D[i][j-1]本内层循环的前一次求出
            D[cur][j]=Math.max(D[pre][j],D[cur][j-1])
        }
    }
}
/*
实际，还可以更进一步的减少空间，使用完全一维的数组，更抽象一点。相对于原始的滚动数组，只保留当前行。
D[j-1]表示D[i][j-1]，当前行计算的前一个值
D[j]表示二维数组的D[i][j](更新后)、D[i-1][j](更新前，是上一轮计算的结果)，迭代更新数组
变量last表示D[i-1][j-1]
*/
int[] D = new int[m+1];
int last;
for(i=1;i<=n;i++){
    //last记录原始D[i-1][j-1],由于D[i-1][0]=0,所以last开始为0
    last=0;
    for(j=1;j<=m;j++){
        //此时的D[j]是D[i-1][j]，保存作为下次计算D[i-1][j-1]
        int temp = D[j];
        if (x[i-1]==y[j-1]) {
            //D[i-1][j-1] 在上次i-1循环已经求出
            D[j]=last+1;
        }else {
            //D[i-1][j] 在上次i-1循环已经求出，D[i][j-1]本内层循环的前一次求出
            //D[j-1]表示原来的D[i][j-1]
            D[j]=Math.max(D[j],D[j-1]);  
        }
        //更新last的值,由于j增加，所以，此时的D[i-1][j]，是下一次计算时D[i-1][j-1]
        last=temp;
    }
}
// 如何输出元素
/*
对于打印公共子序列，可以增加一个二维数组，记录没一个D[i][j]计算时的路径字符
每次计算D[i][j]时，有3种情况：
a. D[i][j]=D[i-1][j-1]+1;此时打印xi
b. D[i][j]=D[i-1][j];递归找
c. D[i][j]=D[i][j-1]；递归找
时间O(n)
*/
```

### 区间动态规划Interval DP

区间DP，枚举区间，把区间分成左右两个部分，然后求出左右区间再合并。

#### 典型：回文问题

```java
/*
1.leetcode516
给定一个字符串 s ，找到其中最长的回文子序列，并返回该序列的长度。可以假设 s 的最大长度为 1000。
分析:
回文特点是，首位2个字母相同，在首尾不同时，对于[i][j]的字符串可以产生2个区间[i][j-1]和[i+1][j]。
因为世界范围是多个区间，而非维度单向的递减，所以，被分做区间动态规划。
1）定义子问题（状态）
D[i][j]是字符串[i:j]范围的最长回文子序列
2）递推公式
若s[i]==s[j],那么D[i][j]=D[i+1][j-1]+2 （如果i>j,则D[i][j]=0）
若s[i]!=s[j],那么D[i][j] =max(D[i+1][j], D[i][j-1])
3）初始情况
单个字符D[i][i]=1,所求D[0][n-1]。
关于递推顺序，可以看到应该先求i大的，然后i减小，而j先求小的，然后在求大的。
所以，两层循环，i循环，从n-1开始，j从i+1开始(j小于i为0，j==i为1)
起始i =n-1, j =n 忽略
起始i =n-2,j =n-1, 若s[i]==s[j], f[n-2][n-1] = f[n-1][n-2]+2，其中f[n-1][n-2]=0
不等，单字符回文数1，max(f[n-1][n-1],f[n-2][n-2])==1

时间，空间开销O(n^2)
*/
public int longestPalindromeSubseq(String s) {
    int n = s.length();
    // 默认值为0
    int[][] f = new int[n][n];
    for (int i = n - 1; i >= 0; i--) {
        f[i][i] = 1;
        for (int j = i + 1; j < n; j++) {
            if (s.charAt(i) == s.charAt(j)) {
                f[i][j] = f[i + 1][j - 1] + 2;
            } else {
                f[i][j] = Math.max(f[i + 1][j], f[i][j - 1]);
            }
        }
    }
    return f[0][n - 1];
}

/*
2. leetcode647
给定一个字符串，你的任务是计算这个字符串中有多少个回文子串。
大问题：一个子串是否是回文串，统计回文串个数
子问题：一个子串是回文串，那么，除去首位，仍然是回文串，所以 


*/



/*
3.给定字符串，找到使其成为回文字符串的最少字符个数
Ab3bd
答案：dAb3bAd or Adb3dbA
插入2个字符(d,A)

1) 定义子问题

D[i][j]是使字符串[i,j]成为回文的最小字符个数
2)

*/

```



 

### 参考

- [【DP专辑】ACM动态规划总结](https://blog.csdn.net/cc_again/article/details/25866971)
- 





### 2.1 斐波那契

入门级：

自顶向下：递归思想+memo想法（记忆化搜索），然后转化为自底向上，即为动态规划。

例子，斐波那契 f(n) = f(n-1) + f(n-2)， 记录每个f(n)避免重复计算（重叠子问题），自底向上，从n=2开始，递推计算。



```java
// leetcode 53
// 最大子序和：给定一个整数数组 nums ，找到一个具有最大和的连续子数组（子数组最少包含一个元素），返回其最大和。
// 思路：动态规划
// 递推，减少问题集大小，化简难度
// f(i)表示以第i个数结尾的连续子数组的最大和，那么max(f(i),0<i<n-1)即所求答案，
// 问题简化了一阶，从两头可变，增加限制以i结尾。
// f(i)的求法，f(i)= max(nms[i]+f(i-1), nums[i])
// 时间复杂度 O(n),空间复杂度O(n)
// 由于f(i) 只与f(i-1)相关，可以用一个变量pre维护f(i-1),用n次比较替换当前max(f(i))，代替n次空间开销，变成空间O(1)。

public int maxSubArray(int[] nums) {
    int pre = 0, maxAns = nums[0];
    for (int x : nums) {
        pre = Math.max(pre + x, x);
        maxAns = Math.max(maxAns, pre);
    }
    return maxAns;
}
// todo:扩展



```

### 2.2 三角形最小路径和

```java
// leetcode 120
// 三角形最小路径和:
// 给定一个三角形 triangle ，找出自顶向下的最小路径和。
// 每一步只能移动到下一行中相邻的结点上。相邻的结点 在这里指的是 下标 与 上一层结点下标 相同或者等于 上一层结点下标 + 1 的两个结点。也就是说，如果正位于当前行的下标 i ，那么下一步可以移动到下一行的下标 i 或 i + 1 。
/*
输入：triangle = [[2],[3,4],[6,5,7],[4,1,8,3]]
输出：11
解释：如下面简图所示：
   2
  3 4
 6 5 7
4 1 8 3
自顶向下的最小路径和为 11（即，2 + 3 + 5 + 1 = 11）。
*/
```

分析

#### 三角形矩阵的表示

三角形矩阵，是非规范矩阵，用vector<vector<integer>> 类型或list<list<integer>>表示，根据常规矩阵\[i\]\[j\]使用习惯，可以将三角形放在第四象限的直角坐标系中，纵坐标为i，方向向下，横坐标为j，方向向右，并将等腰三角左对齐转化为等腰直角三角。示例：

```
-------> j
|1
|2 3
|4 5 6
i
这样，根据三角矩阵的移动特性，f(0,0)转移的两个路径是f(1,0)和f(1,1),并且下一步的搜索空间还是一个小一阶n-1的直角三角型。
```

在能够正常表示三角矩阵，并搜索子空间后，原问题的状态转移方程便可求出：`f(i,j)=min(f(i+1,j),f(i+1,j+1))+A(i,j), 0<=i<n,0<=j<n`问题所求f(0,0)是多少。

```java
// leetcode 120 题解
// 为了计算f(0,0),需要先计算f(1,0)和f(1,1)，递推，i应该从n-2开始，0<=j<i+1,作为最底层，向三角顶点计算f(i,j)，对于f(i,j)只与f(i+1,)有关，与f(i+2,) ，所以，存储空间可以使用A(i,j)本身,无需另外存储。

public int minimumTotal(List<List<Integer>> triangle) {
            int len =  triangle.size();
            for (int i=len -2; i>=0; i-- ) {
                for (int j=0; j < i+1;j++ ) {
                    Integer sum = triangle.get(i).get(j)+ Math.min(triangle.get(i+1).get(j),triangle.get(i+1).get(j+1));
                    triangle.get(i).set(j,sum); 
                }
            }
            return triangle.get(0).get(0);
    }
```





### 2.3 01背包问题

有n个重量和价值分别为wi，vi的武平，从这些物品中提先出总重量不超过W的物品，求价值总和最大值。

1<=n<=100

1<=wi,vi <<100

1<=W<=10000





### 2.4 括号匹配

（pingcap19 面试题目）





## 3.贪心算法

思想：局部最优，也是全局最优。

无后效性，某个状态以前的过程不影响以后的状态，只与当前的状态有关。

数学归纳法、反证法可以证明贪心算法。

题型特点：问题中带有最大/小，最多/少，是否满足可以转化为前者

```java
/*
leetcode455:饼干分配
假设你是一位很棒的家长，想要给你的孩子们一些小饼干。但是，每个孩子最多只能给一块饼干。
对每个孩子 i，都有一个胃口值 g[i]，这是能让孩子们满足胃口的饼干的最小尺寸；并且每块饼干 j，都有一个尺寸 s[j] 。如果 s[j] >= g[i]，我们可以将这个饼干 j 分配给孩子 i ，这个孩子会得到满足。你的目标是尽可能满足越多数量的孩子，并输出这个最大数值。

为什么是贪心算法：
要求满足数量最多的孩子，也是需要将饼干最大化利用。那么从最小大小的饼干开始，给胃口最小的孩子，可以保证饼干最小的被浪费。
证明：假设贪心策略给第i个孩子第m个饼干，并且是满足第i个孩子的最小的饼干。假设选择给第i个孩子，最优解法是饼干n，n大于m，那么使用m代替n，不影响最优策略，后续能使用m给第j个孩子的地方一定可以使用n。所以贪心算法一定可以达到理论保证满足最多的孩子（可能存在多个方案）。
*/
import java.util.Arrays;
public int findContentChilderen(int [] g, int [] s){
    // 从小到大，排序
    Arrays.sort(g);
	Arrays.sort(s);
    int len1 = g.length;
    int len2 = s.length;
    int i=0,j=0;
    while(i<len1 && j< len2){
        if (g[i] <= s[j]){
            i++;
        }
        j++;
    }
    return i;// i即满足孩子的数量
}

/*
tips:Arrays 静态方法
1.toSting
int[] arrInt = {55,44,33,22,11};
Arrays.toString(arrInt);//将数组按照默认格式输出为字符串,[55, 44, 33, 22, 11]
2.sort(Array[] array, int fromIndex, int toIndex)
Arrays.sort(arrInt); //默认升序排序
3.binarySearch(Array[] array, int fromIndex, int toIndex, data key)
int[] arrInt = {55,44,33,22,11};
//使用binarySearch方法前对数组进行排序
Arrays.sort(arrInt);
int  pos = Arrays.binarySearch(arrInt, 44);// return 3
*/


/*
leetcode452:用最少数量的箭引爆气球
在二维空间中有许多球形的气球。对于每个气球，提供的输入是水平方向上，气球直径的开始和结束坐标。由于它是水平的，所以纵坐标并不重要，因此只要知道开始和结束的横坐标就足够了。开始坐标总是小于结束坐标。

一支弓箭可以沿着 x 轴从不同点完全垂直地射出(向y轴无限前进)。在坐标 x 处射出一支箭，若有一个气球的直径的开始和结束坐标为 xstart，xend， 且满足  xstart ≤ x ≤ xend，则该气球会被引爆。可以射出的弓箭的数量没有限制。 弓箭一旦被射出之后，可以无限地前进。我们想找到使得所有气球全部被引爆，所需的弓箭的最小数量。
给你一个数组 points ，其中 points [i] = [xstart,xend] ，返回引爆所有气球所必须射出的最小弓箭数。

输入：points = [[10,16],[2,8],[1,6],[7,12]]
输出：2
解释：对于该样例，x = 6 可以射爆 [2,8],[1,6] 两个气球，以及 x = 11 射爆另外两个气球

分析：
射出的弓箭最小，即每次尽可能引爆最多的气球。
可以模拟，看出将从最小的xend开始，以气球尾部xend[i]为界，可以尽可能的将其他xstart[j]<xend[i]的气球射破。

*/
public int findMinArrowShots(int [][] points){
    if (points.length==0) return 0;
    // 以xend排序，从小到大
    // 整型溢出问题
    //Arrays.sort(points,(a,b)->(a[1]-b[1]));
    // 或者由于等号不影响题目，Arrays.sort(points,(a,b)->(a[1]<b[1]?-1:1));
    Arrays.sort(points,(a,b)->{
        if (a[1] < b[1]){
           return -1;
        } else if (a[1]==b[1]){
           return 0;
        } else return 1;
    });
    
    int curPos = points[0][1];
    int ret = 1;
    for (int i=1;i<points.length;i++){
        if (points[i][0]<=curPos){
            continue;
        }
        curPos = points[i][1];
        ret++;
    }
    return ret;
}

/*
leetcode605:种花问题
假设有一个很长的花坛，一部分地块种植了花，另一部分却没有。可是，花不能种植在相邻的地块上，它们会争夺水源，两者都会死去。

给你一个整数数组  flowerbed 表示花坛，由若干 0 和 1 组成，其中 0 表示没种植花，1 表示种植了花。另有一个数 n ，能否在不打破种植规则的情况下种入 n 朵花？能则返回 true ，不能则返回 false。

分析：
能否种n朵花，使用贪心的思想是，尽可能的种花，若可以种下n朵花，表示符合。
尽可能种花，最大化情况下是，只间隔一朵。
*/
public boolean canPlaceFlowers(int[] flowerbed,int n){
    int len = flowerbed.length;
    // -1位置，预先为0
    int pre = 0;
    for (int i=0;i<len && n > 0;i++){
        if (pre==0&&flowerbed[i]==0
            && (i==len-1 || flowerbed[i+1]==0)){
            n--;
            // 当前位置种花
            flowerbed[i]=1;
        }
        pre = flowerbed[i];
    }
    return n==0;
}

/*
leetcode122.买卖股票的最佳时机 II
给定一个数组 prices ，其中 prices[i] 是一支给定股票第 i 天的价格。
设计一个算法来计算你所能获取的最大利润。你可以尽可能地完成更多的交易（多次买卖一支股票）。
注意：你不能同时参与多笔交易（你必须在再次购买前出售掉之前的股票）。
分析：
利润最大，即每次低买高买，吃掉波动中的所有上升阶段，忽略掉下降阶段。

*/
public int maxProfit(int[] prices) {
    int profit =0;
    for(int i=1;i< prices.length;i++){
        profit+=Math.max(0,prices[i]-prices[i-1]);
    }
    return profit;
}

/*
leetcode860:柠檬水找零
在柠檬水摊上，每一杯柠檬水的售价为 5 美元。
顾客排队购买你的产品，（按账单 bills 支付的顺序）一次购买一杯。
每位顾客只买一杯柠檬水，然后向你付 5 美元、10 美元或 20 美元。你必须给每个顾客正确找零，也就是说净交易是每位顾客向你支付 5 美元。
注意，一开始你手头没有任何零钱。
如果你能给每位顾客正确找零，返回 true ，否则返回 false 。
分析：
分类讨论
支付5元，无需找零;
支付10元，需要找零5;
支付20元，需要找零10(5+5)+5元;同时20不可用于找零。
要能尽可能能找零，应在给20找零时先用10元，再用5元。
*/
public boolean lemonadeChange(int[] bills) {
    int cnt5=0;
    int cnt10=0;
    // for (int bill : bills) {
    for (int i=0;i < bills.length;i++){
        if (bills[i] == 5){
            cnt5++;
        }else if (bills[i]==10){
            if (cnt5>0){
                cnt10++;
                cnt5--;
            }else {
                return false;
            }
        } else {
            if (cnt10>0 && cnt5 > 0){
                cnt10--;
                cnt5--;
            }else if (cnt5 >= 3){
                cnt5-=3;
            }else {
                return false;
            }
        }
    }
    return true;
}

```



## 4.排序算法

### 4.1 快速排序



### 4.2 归并排序





## 树



## 数据结构



### 位运算

```c++
/*
原码：符号位和二进制数的绝对值
反码：正数的反码等于其原码，负数的反码是其原码除符号位外，按位取反。
补码：正数的补码等于其原码，负数的补码是其反码加1。
计算机中的二进制是用补码表示。
补码直接计算使用溢出原理，保证正确。
最小值：1000000... =-2^(N-1), 11111... = -1 
*/


/* 剑指10：二进制1的个数
实现函数，输入整数，输出该数二进制表示中1的个数
陷阱：右移位，检查最右位是否为1，负数，导致循环。
解法1：使用无符号，32为整形1，逐一试探没一位，O(n)
*/
int NumberOf1(int n) {
    int count =0;
    unsinned int flag =1;
    // 循环32次
    while(flag) {
        if (n&flag){
            count++;
        }
        flag = flag <<1;
    }
    return count;
}
/*
解法2：
技巧：把一个整数减去1，再和原整数做与运算，会把原整数最右边一个1变成0。
边界测试：正数（1,0x7FFFF），负数(0x80000,0xFFFFFF)，0
*/
int NumberOf1(int n) {
	int count = 0;
    while(n){
        count++;
        n=(n-1)&n;
    }
    return count;
}

/*
利用解法2的技巧，可以判断相似问题
- 判断一个整数是不是2的整数次方（二进制中有且只有一位是1）
- 输入两个整数m和n，计算该变m的二进制多少位，才能等到n。分成2步，第一步m异或n，第二步计算结果中1的个数。
*/

/*
剑指47：位运算的加法
原理：位相加，不考虑进位，等于异或。
进位是1+1,情况，等于与操作，然后左移1位。
最后，将进位与异或结果相加，相加过程重复前两部，知道无进位。
*/
int BitAdd(int num1, int num2){
    int sum,carry;
    while(num2!=0) {
        sum = num1^num2;
        carrry = (num1 & num2) <<1;
        
        num1=sum;
        num2=carry;
    }
    return num1;
}

// 交换2个变量的值,不使用新变量
// 基于加减      基于异或(a^a=0,a^0=a)
// a=a+b;       a=a^b;
// b=a-b;		b=a^b;(a^b^b=a)
// a=a-b;		a=a^b;(a^b^a=b)


```





### 并查集



### 跳表SkipList

### 二叉树树

### B树



### 数组

### 哈希表

### 栈与队列

### 字符串





