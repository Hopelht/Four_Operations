
| 课程名称 |   [软件工程](https://bbs.csdn.net/forums/gdut-ryuezh)   |
|    :-:    |   :-:   |
| 作业要求	|   [结对编程：小学四则运算](https://bbs.csdn.net/topics/608268113)	 |
| GitHub	|    [仓库地址]()       |
| 项目成员	|   丁冠智3120002096      钟华峥3120005133       |

<br>

@[TOC]

<br>

# 一、PSP表格

| PSP2.1|Personal Software Process Stages|预估耗时（分钟）|实际耗时（分钟） |
|  :-  | :-  |  :-:  |  :-:  |
| Planning|计划 | 20  |10    |
|  · Estimate|· 估计这个任务需要多少时间| 30 |  30  |
|Development|开发| 300  |  220  |
|· Analysis|· 需求分析 (包括学习新技术)|30  |   10 |
|· Design Spec|· 生成设计文档|20  | 20   |
|· Design Review|· 设计复审|20  |   5 |
|· Coding Standard|· 代码规范 (为目前的开发制定合适的规范)|10  |  20  |
|· Design|· 具体设计|20  |  20  |
|· Coding|· 具体编码|100  |  90  |
|· Code Review|· 代码复审|10  |  5  |
|· Test|· 测试（自我测试，修改代码，提交修改）| 30  |  30  |
|Reporting|报告|30  |   30 |
|· Test Repor|· 测试报告|10  |  5  |
|· Size Measurement|· 计算工作量|10  |  5  |
|· Postmortem & Process Improvement Plan|· 事后总结, 并提出过程改进计划|  20  |  10  |
|| · 合计   |  660   |   510    |

<br>

# 二、任务分析
1. 使用 -n 参数控制生成题目的个数，例如`Myapp.exe -n 10`；
2. 使用 -r 参数控制题目中数值(自然数、真分数和真分数分母)的范围，例如`Myapp.exe -r 10`；
3. 每道题目中出现的运算符个数不超过3个;
4. 生成的题目中计算过程不能产生负数，即算术表达式中若存在形如`e1−e2`的子表达式，那么`e1≥e2`；
5. 生成的题目中如果存在形如`e1÷e2`的子表达式，那么其结果应是真分数；
6. 程序一次运行生成的题目不能重复，即任何两道题目不能通过有限次交换+和×左右的算术表达式变换为同一道题目；
7. 生成的题目存入执行程序的当前目录下的Exercises.txt文件，格式如下：
> 1. 四则运算题目1
> 2. 四则运算题目2
> 3. 四则运算题目3
8. 在生成题目的同时，计算出所有题目的答案，并存入执行程序的当前目录下的Answers.txt文件，格式如下：
> 1. 答案1
> 2. 答案2
> 3. 答案3
10. 程序支持对给定的题目文件和答案文件，判定答案中的对错并进行数量统计，统计结果输出到文件Grade.txt，输入参数格式及统计结果格式如下：
> 输入参数：`Myapp.exe -e <exercisefile>.txt -a <answerfile>.txt`<br>
> 统计格式：
> Correct: 5 (1, 3, 5, 7, 9)
> Wrong: 5 (2, 4, 6, 8, 10)

11. 程序应能支持一万道题目的生成。

<br>

# 三、实现流程
## 3.1 系统流程图
> 该系统采取了面向对象的方法进行设计编程，按照`生成题目`、`计算答案`、`校对答案`这三个功能将系统分为了三个模块，并且构造了四个类和一个函数，下面的流程图是四个类之间的作用关系。

![在这里插入图片描述](https://img-blog.csdnimg.cn/1af8c4ab491645fd87ef66ea24c26373.png)


<br>

## 3.2 Binary_Tree类
> BinaryTree类采用了基于二叉树的形式进行查重，目的是避免Question类生成重复的表达式，主要实现了两个功能：
> * 生成二叉树：利用二叉树存储传入的后缀表达式列表
> * 检查两棵二叉树是否相同：利用递归进行结点的遍历

```python
import operator

# 用于存储4则运算规则以及判断表达式是否相同

class Tree_Node:  # 二叉树的结点
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class Binary_Tree:
    def __init__(self):
        self.tree_stack = []  # 二叉树
        self.expression = []  # 表达式

    def generateBinaryTree(self, exp):  # 生成二叉树
        self.expression = exp
        for item in self.expression:
            parent = Tree_Node(item)
            if not item in ['+', '-', 'x', '÷']:
                # 操作数
                self.tree_stack.append(parent)
            else:
                # 运算符
                right = self.tree_stack.pop()
                left = self.tree_stack.pop()
                parent.right = right
                parent.left = left
                self.tree_stack.append(parent)

        # 二叉树的根
        parent = self.tree_stack[-1]
        return parent

    def isSame(self, root):  # 判断二叉树是否相同
        if not root.left:
            if not root.right:
                return root.value
        elif root.value == '+' or root.value == 'x':
            left = self.isSame(root.left)
            right = self.isSame(root.right)
            if operator.le(left, right):
                return root.value + left + right
            else:
                return root.value + right + left
        else:
            return root.value + self.isSame(root.left) + self.isSame(root.right)
```
<br>

## 3.3 Expression类
> Expression类实现了两个功能：
> * 将中缀表达式转化为后缀表达式（ `def toSuffix(self) `）
> * 计算后缀表达式的值（ `def suffixToValue(self)` ）
> 例如后缀表达式“1 2 3 + 4 * + 5 -”：（参考博客：[后缀表达式](https://blog.csdn.net/North_City_/article/details/119281826?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522166447075016782395358933%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=166447075016782395358933&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~top_click~default-3-119281826-null-null.142%5Ev51%5Eopensearch_v2,201%5Ev3%5Eadd_ask&utm_term=%E5%90%8E%E7%BC%80%E8%A1%A8%E8%BE%BE%E5%BC%8F&spm=1018.2226.3001.4187)）
(1) 从左至右扫描，将1和2和3压入堆栈；
(2) 遇到+运算符，因此弹出3和2（3为栈顶元素，2为次顶元素，注意与前缀表达式做比较），计算出3+2的值，得5，再将5入栈；
(3) 将4入栈；
(4) 接下来是×运算符，因此弹出4和5，计算出4×5=20，将20入栈；
(5) 接下来是+运算符，弹出20和1，计算20+1=21，将21入栈；
(6) 将5入栈；
(6) 最后是-运算符，计算出21-5的值，即16，由此得出最终结果。

```python
from fractions import Fraction

# 后缀表达式转换
class suffix_expression:  #     将中缀表达式转化为后缀表达式，计算后缀表达式的值
    def __init__(self, exp):  # 类的构造函数
        self.exp = exp
        self.re = self.toSuffix()
        self.value = self.suffixToValue()

    def toSuffix(self): # exp: 表达式字符串
        if not self.exp:
            return []
        ops_rule = {
            '+': 1,
            '-': 1,
            '×': 2,
            '÷': 2,
        }
        suffix_stack = []  # 后缀表达式结果
        ops_stack = []  # 操作符栈
        infix = self.exp.split(' ')  # 将表达式分割得到单词
        for item in infix:

            if item in ['+', '-', '×', '÷']:  # 遇到运算符
                while len(ops_stack) >= 0:
                    if len(ops_stack) == 0:
                        ops_stack.append(item)
                        break
                    op = ops_stack.pop()
                    if op == '(' or ops_rule[item] > ops_rule[op]:
                        ops_stack.append(op)
                        ops_stack.append(item)
                        break
                    else:
                        suffix_stack.append(op)
            elif item == '(':  # 左括号直接入栈
                ops_stack.append(item)
            elif item == ')':  # 右括号
                while len(ops_stack) > 0:
                    op = ops_stack.pop()
                    if op == "(":  # 一直搜索到出现“(”为止
                        break
                    else:
                        suffix_stack.append(op)
            else:
                suffix_stack.append(item)  # 数值直接入栈

        while len(ops_stack) > 0:
            suffix_stack.append(ops_stack.pop())

        self.re = suffix_stack
        return suffix_stack

    def suffixToValue(self):  # 后缀表达式求值
        stack_value = []
        for item in self.re:
            if item in ['+', '-', '×', '÷']:
                n2 = stack_value.pop()
                n1 = stack_value.pop()
                result = self.cal(n1, n2, item)
                # print("resule:{}".format(result))
                # 求值过程中出现负数和n/0这个情况去除
                if result < 0 or result == False:
                    return False
                stack_value.append(result)
            else:
                if item.find('/') > 0:
                    attach = 0
                    right = ""
                    if item.find("'") > 0:
                        parts = item.split("'")
                        attach = int(parts[0])
                        right = parts[1]
                    else:
                        right = item
                    parts = right.split('/')
                    result = Fraction(attach * int(parts[1]) + int(parts[0]), int(parts[1]))
                    stack_value.append(result)
                else:
                    stack_value.append(Fraction(int(item), 1))

        return stack_value[0]

    def cal(self, n1, n2, op):   # 建立4则表达式
        if op == '+':
            return n1 + n2
        if op == '-':
            return n1 - n2
        if op == '×':
            return n1 * n2
        if op == '÷':
            if n2 == 0:
                return False
            return n1 / n2

```

> 中缀表达式转化为后缀表达式的算法采用了栈的思想进行处理，定义了后缀表达式栈`suffix_stack[]`和操作符栈`ops_stack[]`，分别用来存放( /取出 )操作数和操作符

<br>

## 3.4 Question类
> Question类实现了生成题目要求的四则运算式子的功能；
> 对于运算式的各个要素（整数、分数、括号、运算符），系统采用了各自的构建方法生成；
> 较为复杂的算法是**分数的生成(假分数转换为带分数)** 和 **运算式查重(避免生成运算本质相同的式子)**

```python
# 构建分数
    def get_range_dec(self):  # 随机生成分数
        operRange = self.oper_range
        while True:
            # 随机生成两个随机数
            operNum1 = self.get_random_num(operRange)
            operNum2 = self.get_random_num(operRange)
            # 判断operNum1是否为operNum2的倍数，若是则重新生成随机数
            if (operNum1 % operNum2) == 0:
                continue
            # 若operNum1不是operNum2的倍数则已获取到符合要求的 operNum1和 operNum2，退出循环
            else:
                break
        # 将获取到的分子和分母进行化简并返回
        return self.stacdardDec(operNum1, operNum2)

    def stacdardDec(self, operNum1, operNum2):  # 化简分数  接收分子 分母参数
        num = Fraction(operNum1, operNum2)
        Num1 = int(num.numerator)
        Num2 = int(num.denominator)
        return [Num1, Num2]

    def get_factor_list(self, oper):  # 获取正整数的公因子包括其本身
        l = []
        for k in range(2, oper + 1):
            if (oper % k) == 0:
                l.append(k)
        return l
```

```python
# 运算式查重
def isRepeat(self, express_set, expression):  # express_set: 表达式集合  # expression: 生成的表达式
    suffixExpression = SuffixExpression(expression)
    target_exp_suffix = suffixExpression.re  # 后缀表达式列表
    binaryTree = BinaryTree()
    target_exp_binary_tree = binaryTree.generateBinaryTree(target_exp_suffix)
    for item in express_set:
        suffixExpression2 = SuffixExpression(item)
        source_exp_suffix = suffixExpression2.re
        source_exp_binary_tree = binaryTree.generateBinaryTree(source_exp_suffix)
        if binaryTree.isSame(target_exp_binary_tree) == binaryTree.isSame(source_exp_binary_tree):
            return True
    return False
```

<br>

## 3.5 Answer类
> Answer类实现功能：
> * 计算答案并写入文档（调用了`SuffixExpression类`）

```python
class Answer:
    def __init__(self, a_path):  # 类的构造函数
        self.exp_list = []
        self.exercisefile = ""
        self.answerfile = ""
        self.a_path = a_path

    def expression_result(self, exp_list):  # 求表达式的结果
        self.exp_list = exp_list  # 表达式列表
        if os.path.exists(self.a_path):  # 清空上一次的答案
            with open(self.a_path, 'r+') as file:
                file.truncate(0)

        for i, exp in enumerate(self.exp_list):
            order_str = str(i + 1)
            suffixExpression = suffix_expression(exp)
            exp_value = str(suffixExpression.suffixToValue()) + '\n'
            result = "Answer" + order_str + ': ' + exp_value

            with open(self.a_path, 'a+', encoding='utf-8') as f:
                f.write(result)

```
<br>


## 3.6 check_answer()函数
> check_answer()函数实现功能：
> * 校对答案（设置了异常处理防止打开文件时出现问题而导致程序出错）

```python
def check_answer(exercisefile, answerfile):  # 检查答案
    wrong_num = 0
    correct_num = 0
    exercise_answer = []
    correct_list = []  # 正确题目序号
    wrong_list = []  # 错误题目序号
    try:
        with open(exercisefile, 'r', encoding='utf-8') as f:
            for line in f:
                # 匹配出正则表达式
                exp_str = re.findall(r'Question\d+: (.*) =\n', line)
                if exp_str:
                    exp = exp_str[0]
                else:
                    continue
                p = suffix_expression(exp)
                exp_value = str(p.suffixToValue())
                exercise_answer.append(exp_value)
    except IOError:
        print('please check if the path is correct')

    # 判断表达式列表是否为空
    try:
        with open(answerfile, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                ans_str = re.findall(r'Answer\d+: (.*)\n', line)
                # 容错
                if ans_str:
                    ans = ans_str[0]
                else:
                    continue
                # 判断是否正确
                if ans == exercise_answer[i]:
                    correct_num += 1
                    correct_list.append(i + 1)
                else:
                    wrong_num += 1
                    wrong_list.append(i + 1)
        with open('Grade.txt', 'w+', encoding='utf-8') as f:   # 生成grade.txt文件成绩
            correct_str = 'Correct: ' + str(correct_num) + ' ' + str(correct_list) + '\n'
            wrong_str = 'Wrong: ' + str(wrong_num) + ' ' + str(wrong_list)
            print(correct_str)
            print(wrong_str)
            f.write(correct_str)
            f.write(wrong_str)
    except IOError:
        print('please check if the path is correct')



if __name__ == '__main__':
    e_path = input("请输入题目文件路径：")
    a_path = input("请输入答案文件路径：")
    if not os.path.exists(e_path):
        print("题目路径不存在！请重新输入")
        exit()
    if not os.path.exists(a_path):
        print("题目路径不存在！请重新输入")
        exit()
    check_answer(e_path,a_path)
```

# 四、性能分析
+ 使用pycharm自带的profile功能进行性能分析。（参考博客：[Pycharm图形化性能测试工具Profile](https://blog.csdn.net/Castlehe/article/details/118088763?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522166360247316782417072897%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=166360247316782417072897&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduend~default-1-118088763-null-null.142%5Ev47%5Epc_rank_34_2,201%5Ev3%5Econtrol_1&utm_term=pycharm%20profile&spm=1018.2226.3001.4187)）
+ 在运行编辑中设置好形参参数：
![在这里插入图片描述](https://img-blog.csdnimg.cn/d25bfd9d0dad4e329cc9a90f72e7d10a.png)

+ 程序运行消耗时间
![在这里插入图片描述](https://img-blog.csdnimg.cn/a7c9cd880ba04634a82d1671b74aa83b.png)
+ 生成树状图可知消耗内存和时间较多的是main.py中的_init_，主要原因是调用各类时进行初始化的变量中调用了类函数获取变量值
![在这里插入图片描述](https://img-blog.csdnimg.cn/7edf166f44a149e29e4f8653ebbf9c67.png)






<br>

# 五、单元测试
## 5.1 使用说明
+ 在命令行中输入如下命令调用main.py可以调用程序生成题目和正确答案，注意-n、-r、-e、-a的参数，缺少要求重新输入
![在这里插入图片描述](https://img-blog.csdnimg.cn/0839a495a6cf43429dc3241c84c2c0b4.png)
+ 在命令行中输入如下命令调用Check.py可以调用程序校验正确答案和自己做的答案，得到统计结果![在这里插入图片描述](https://img-blog.csdnimg.cn/e5730397fe2f4919977eb6afc9338368.png)

## 5.2题目和答案生成
+ 命令行输入上述正确例示之后，可以生成题目文件和答案文件，分别存放在data_save/Exercises.txt和data_save/Answer.txt中。满足任务分析中的要求1到9。

![在这里插入图片描述](https://img-blog.csdnimg.cn/21a5f4de695c483f854cde59930f849a.png)![在这里插入图片描述](https://img-blog.csdnimg.cn/2f32d789f6de4aa68313b3c0478d170c.png)



## 5.2 答案校对统计
+ 命令行输入上述正确例示之后，可以校对自己的答案和正确答案，自己的答案存放在data_save/student_answer.txt中。生成统计结果，存放在Grade.txt中。满足任务分析中的要求10。

![在这里插入图片描述](https://img-blog.csdnimg.cn/e8552d41f494474d90ec1a323308ee8e.png)![在这里插入图片描述](https://img-blog.csdnimg.cn/0bcbb57470c34f08b2e0e843084212e9.png)
## 5.3 生成一万道题目
![在这里插入图片描述](https://img-blog.csdnimg.cn/6e111a5ae839430293a48e42bec2af5b.png)![在这里插入图片描述](https://img-blog.csdnimg.cn/a99201f82d6b4b52b6aa522c0dfd99e4.png)



<br>

# 六、项目小结
本次结对编程提供了两个人的角度去解决问题，而不会让思维仅仅局限于一个人的想法之中。既可以提高工作效率，也可以锻炼思维的发散性。项目中主要用到二叉树，列表，栈的数据结构，并要将我们平时看到的数学公式（中缀表达式）转化为后缀表达式。总的来说，在本次的编程项目里，不仅提高了团队中每个人的编程能力，同时也锻炼了每个人的合作能力，交流能力，表达能力，也相互借鉴学习了彼此身上的优点。
