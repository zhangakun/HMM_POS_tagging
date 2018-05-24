# 基于HMM的词性标注
> 2018-5-23
> 
> 编写环境: Python-3.6 macOS-10.13
> 
> 
> 
> [TOC]

似乎github解析不了markdown里的LaTeX公式，点击[这里](https://zenuora.github.io/HMM_POS_tagging/README.html)查看html形式 

## 文件结构

```
.
├── data
│   ├── 1998 //此文件夹下的原始语料用作 训练数据
│   │   └── 199801.txt  
│   ├── corpus_readme.pdf  //语料库使用说明书
│   ├── 199806.txt    //原始语料，用于生成下面两个文件
│   ├── for_eval_199806#part.txt  //用于评分的 标准标注数据
│   └── for_test_199806#part.txt  //用于测试的 未标注数据
├── eval.py     //评分
├── model
│   ├── prob_emit.json
│   ├── prob_start.json
│   ├── prob_trans.json
│   ├── tag_set.txt     //标注集，从训练数据中取得
│   └── word_set.txt    //登录词集，从训练数据中取得
├── output
│   ├── result.txt //测试后的结果
│   ├── score.txt  //评分后的结果
│   └── unregister.txt  //测试后，取得的测试数据中的未登录词
├── prepare.py  //准备用于 测试和评分的数据
├── test.py     //测试
└── train.py    //训练
```

## 使用流程
==在HMM目录下，使用终端/命令行==

![屏幕快照 2018-05-24 00.16.06](media/15270483022210/%E5%B1%8F%E5%B9%95%E5%BF%AB%E7%85%A7%202018-05-24%2000.16.06.png)

### 0.准备
执行命令：`python3 prepare.py`

准备用于 测试和评分的数据，输出到data目录下

![屏幕快照 2018-05-24 00.16.26](media/15270483022210/%E5%B1%8F%E5%B9%95%E5%BF%AB%E7%85%A7%202018-05-24%2000.16.26.png)

### 1.训练
执行命令：`python3 train.py`

使用训练数据（data/1998/目录下），来获取HMM模型参数

训练完成后，在model目录下生成三个概率参数json文件 和 登录词集，标注集：
![屏幕快照 2018-05-24 00.17.55](media/15270483022210/%E5%B1%8F%E5%B9%95%E5%BF%AB%E7%85%A7%202018-05-24%2000.17.55.png)
![屏幕快照 2018-05-24 00.20.36](media/15270483022210/%E5%B1%8F%E5%B9%95%E5%BF%AB%E7%85%A7%202018-05-24%2000.20.36.png)
![屏幕快照 2018-05-24 00.20.42](media/15270483022210/%E5%B1%8F%E5%B9%95%E5%BF%AB%E7%85%A7%202018-05-24%2000.20.42.png)


### 2.测试
执行命令：`python3 test.py`

使用model目录下的HMM模型参数，来对测试数据（./data/for_test_199806#part.txt）进行标注

测试后，结果和未登录词集 输出到output目录下
![屏幕快照 2018-05-24 00.19.12](media/15270483022210/%E5%B1%8F%E5%B9%95%E5%BF%AB%E7%85%A7%202018-05-24%2000.19.12.png)
![屏幕快照 2018-05-24 00.20.25](media/15270483022210/%E5%B1%8F%E5%B9%95%E5%BF%AB%E7%85%A7%202018-05-24%2000.20.25.png)
测试结果中，若某词未登录，则在预测的标注后加'?'，方便后续评分中得到未登录词的标注正确率

![屏幕快照 2018-05-24 00.20.15](media/15270483022210/%E5%B1%8F%E5%B9%95%E5%BF%AB%E7%85%A7%202018-05-24%2000.20.15.png)

### 3.评分

执行命令：`python3 eval.py`

比较测试结果（result.txt）和标准分词答案（for_eval_199806#part.txt）的区别

评分结果输出到output目录下（score.txt）
![屏幕快照 2018-05-24 00.19.48](media/15270483022210/%E5%B1%8F%E5%B9%95%E5%BF%AB%E7%85%A7%202018-05-24%2000.19.48.png)

![屏幕快照 2018-05-24 00.20.06](media/15270483022210/%E5%B1%8F%E5%B9%95%E5%BF%AB%E7%85%A7%202018-05-24%2000.20.06.png)



## 实现原理

### 词性标注
采用部分的『1998年人民日报语料库』来训练模型。

其中用了42个词性标注：见 ./model/tag_set.txt（每次运行train.py会自动生成）

具体含义见 ./data/corpus_readme.pdf

### 隐马尔可夫模型

![HM-w700](media/15258821120351/HMM.png)

由于训练数据已经标注，因此采用**直接统计的方法**来获取隐马尔可夫模型的参数。

### Viterbi算法
通常用于解决，HMM中典型问题：假设给定HMM，共有S个状态，用$1,2,...,S$编号表示。初始状态为i的概率是$\pi_i$，从状态i到j的转移概率为$a_{i,j}$。现观察到的输出序列为$y_1,y_2,...,y_T$。求产生观察结果的最有可能的状态序列$x_1,x_2,...,x_T$


实质是一种**动态规划算法**，其最优值的递归定义如下：
\\[
V[t][k] =
\begin{cases}
P(y_1|k)\cdot\pi_k &  t=1\\
\max_{1\le x \le S}\{\;P(y_t|k)\cdot a_{x,k}\cdot V[t-1][x]\;\} &  t>1
\end{cases}
\\]

最优值$V[t][k]$的含义：
对于前t个输出，有多个的 长度为t状态序列 可以与之对应。这些状态序列的概率不同。$V[t][k]$表示『第t个输出对应的状态是k』的一组状态序列中 概率最大的那个概率

每次计算$\max_{1\le x \le S}\{...\}$时，需要记录下最终选取的前一个状态x，以便最后构造最优解

构造最优解（最优状态序列）：
由$\max_{1\le k \le S}\{V[T][k]\}$，求得最优状态序列的第T个状态$k=x_T$，然后取得$V[T][x_T]$记录的前一个状态$x_{T-1}$，然后取得$V[T-1][x_{T-1}]$记录的前一个状态$x_{T-2}$，……

### 未登录词的影响
若$y_t$是未登录的输出，则$P(y_1|k)_{1\le k \le S}=0$，会使$V[t][k]_{1\le k \le S}$均为0，而后$V[m][k]_{t\le m \le T,1\le k \le S}$也均为0。这样，最后构造的最优解无意义。

#### 解决方案：
举个栗子：对于观察到的长度为2的输出序列$y_1y_2$，若已经求得所有$V[1][k]_{1\le k \le S}$，而$y_2$为未登录的输出。求产生观察结果的最有可能的状态序列$x_1x_2$。

==由于之前从未识别过$y_2$，只能依靠 前一个状态$x_1$和$x_1$的转移概率 来近似猜测$x_2$。==

==所以，若$x_1=x$，求$x_2$的近似概率分布：$\{P(x_2=k) \approx P(x_1=x)\cdot a_{x,k}\;| 1\le k \le S\}$==

实际做法中，应该使$V[2][k]=\max_{1\le x \le S}\{\;a_{x,k}\cdot V[1][x]\;\} $

其中，$V[2][k]_{1\le k \le S}$，表示 『第2个输出对应的状态是k』的一组状态序列 中概率最大的那个序列的概率。


### 计算精度的影响
由于数据量规模较大，使得计算出来的概率都十分小。而极小的概率相乘，有可能产生下溢或被截断为0，并且计算开销很大。

#### 解决方案：
可对上述参数和参数的计算，都取自然对数进行处理。

另外，由于取对数的每个概率值不能为0：

* 若求得的概率值极小而被截断为0，则直接取为-1000表示很小的概率
* 若概率值本来就为0，则直接取为-10000表示为0的概率

事实上，运算采用对数，就解决了『由于未登录词的放射概率为0，相乘导致的后续$V[m][k]_{t\le m \le T,1\le k \le S}$也均为0』的问题


## 代码实现
### prepare.py
```python
import re

if __name__ == "__main__":
    count = 0
    
    with open("./data/199806.txt", 'r')as r, open("./data/for_test_199806#part.txt", 'w')as t, open(
            "./data/for_eval_199806#part.txt", 'w')as s:
        for line in r:
            line = re.sub(r'\[|\][a-z]+', '', line).strip()
            if not line: continue

            count += 1
            # 只取1000句，用作测试数据
            if count > 1000:
                break

            word_tag_list = line.split()[1:]
            s.write("  ".join(word_tag_list) + "\n")

            word_list = []
            for i in list(range(len(word_tag_list))):
                arr = word_tag_list[i].split('/')
                if len(arr) >= 2:
                    word_list.append(arr[0])

            t.write("  ".join(word_list) + "\n")
```
### train.py
```python
# 将参数输出到模型
def output():...

# 直接统计发射概率，初始状态，转移概率
def train(file):...

if __name__ == "__main__":
    path = "./data/1998"

    for file in os.listdir(path):
        file = os.path.join(path, file)
        if os.path.isfile(file) and os.path.splitext(file)[1] == '.txt':
            train(file)

    output()
```
### test.py
```python
# 从文件中，加载模型
def load_model():...

# 利用HMM模型，获得标注序列
def viterbi(obs):...

# 将标注序列，转换为标注结果输出
def tag(sentence):...

if __name__ == "__main__":
    load_model()

    line_num = 0
    with open("./data/for_test_199806#part.txt") as test_f, open("./output/result.txt", 'w') as result_f:
        for line in test_f:
            line = line.strip()
            if not line:
                continue
            line_num += 1
            if line_num % 10 == 0:
                print(line_num)
            result_f.write(tag(line))

    with open("./output/unregister.txt", 'w')as unreg_f:
        unreg_f.write("共找到%s个未登录词，分布于%s个句子中\n\n"%(unreg_total,unreg_line_num))
        unreg_f.write("\n".join(unreg_out))
```
### eval.py
```python
import re
import sys

if __name__ == "__main__":
    total = 0
    corr = 0
    unreg_total = 0
    unreg_corr = 0

    with open("./output/result.txt", 'r')as r, open("./data/for_eval_199806#part.txt")as e, open("./output/score.txt", 'w')as s:
        for line in e:
            linee = line.strip()
            if not linee: continue

            while True:
                liner = r.readline().strip()
                if liner: break

            linee = linee.split()
            liner = liner.split()

            err = False

            if len(linee) != len(liner):
                print('err!')
                continue
            else:
                total += len(linee)
                for i in range(len(linee)):
                    is_unreg = False
                    if liner[i][-1] == '?':
                        is_unreg = True
                        unreg_total += 1
                        liner[i] = liner[i][:-1]
                    if linee[i] == liner[i]:
                        corr += 1
                        if is_unreg: unreg_corr += 1
                    else:
                        err = True
                        s.write("not your result: %s ,but: %s \n" % (liner[i], linee[i]))
                if err:
                    s.write(line + '-----------------------\n\n')

        s.write("\n\n[最终结果]\n\n给%s个词做词性标注，对了%s个。\n标注正确率：%s" % (total, corr, corr * 1.0 / total))

        if unreg_total:
            s.write("\n\n%s个词中，未登录词有%s个，对了%s个。\n未登录词出现率：%s\n未登录词标注正确率：%s\n\n" % (
                total, unreg_total, unreg_corr, unreg_total * 1.0 / total, unreg_corr * 1.0 / unreg_total))

```



