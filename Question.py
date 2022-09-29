import random
from fractions import Fraction
import os
from Expression import suffix_expression
from BinaryTree import Binary_Tree


# 生成问题类
class Question:
    def __init__(self, expression_num, oper_range, _path):  # 类的构造函数
        self.oper_range = oper_range  # 操作数范围
        self.oper_count = 3  # 操作符个数
        self.e_path = _path
        dec_chance = random.randint(1, 10) / 100  # 减少生成分数题目数量
        self.dec_chance = dec_chance  # 出现分数的概率
        self.expression_num = expression_num  # 生成表达式的数目
        self.problem_array = self.create_question()   # 表达式列表表示
        self.normalize_expression(self.problem_array, self.e_path)

    def create_question(self):  # 表达式生成主函数
        exp_num = self.expression_num     # 生成表达式的数目
        expression_list = []
        i = 0

        while i < exp_num:
            random_num_operation = random.randint(1, self.oper_count)  # 运算符的数目
            is_need_parenteses = random.randint(0, 1)  # 是否需要加括号
            number_of_oprand = random_num_operation + 1  # 操作数比操作符的数目多1
            exp = []
            for j in range(random_num_operation + number_of_oprand):
                if j % 2 == 0:
                    # 随机生成操作数(含分数)
                    exp.append(self.get_oper_num()['operStr'])

                    if j > 1 and exp[j - 1] == '÷' and exp[j] == '0':
                        while True:
                            exp[j - 1] = self.generate_operation()
                            if exp[j - 1] == '÷':
                                continue
                            else:
                                break
                else:
                    # 生成运算符
                    exp.append(self.generate_operation())

                if j > 3:
                    if exp[j - 2] == '÷':  #
                        if exp[j - 1] > exp[j - 3]:
                            t = exp[j - 1]
                            exp[j - 1] = exp[j - 3]
                            exp[j - 3] = t


                    elif exp[j - 2] == '-':
                        if exp[j - 1] < exp[j - 3]:
                            t = exp[j - 1]
                            exp[j - 1] = exp[j - 3]
                            exp[j - 3] = t

            # 判断是否要括号
            if is_need_parenteses and number_of_oprand != 2:
                expression = " ".join(self.generate_parentheses(exp, number_of_oprand))
            else:
                expression = " ".join(exp)

            # 判断是否有重复
            if self.expression_num <= 500:
                if self.isRepeat(expression_list, expression):
                    continue
                else:
                    result = self.calculate(expression)
                    if result == "False":
                        pass
                    else:

                        expression_list.append(expression)
                        i = i + 1
            else:
                result = self.calculate(expression)
                if result == "False":
                    pass
                else:
                    expression_list.append(expression)
                    i = i + 1

        return expression_list

    def generate_operation(self):  # 随机生成操作符
        operators = ['+', '-', '×', '÷']
        return operators[random.randint(0, len(operators) - 1)]

    def generate_parentheses(self, exp, number_of_oprand): # exp: 表达式  number_of_oprand: 运算符数目
        expression = []
        num = number_of_oprand
        if exp:
            exp_length = len(exp)
            left_position = random.randint(0, int(num / 2))
            right_position = random.randint(left_position + 1, int(num / 2) + 1)
            mark = -1
            for i in range(exp_length):
                if exp[i] in ['+', '-', '×', '÷']:
                    expression.append(exp[i])
                else:
                    mark += 1
                    if mark == left_position:
                        expression.append('(')
                        expression.append(exp[i])
                    elif mark == right_position:
                        expression.append(exp[i])
                        expression.append(')')
                    else:
                        expression.append(exp[i])
        # 如果生成的括号表达式不符合题意就重新生成
        if expression[0] == '(' and expression[-1] == ')':
            expression = self.generate_parentheses(exp, number_of_oprand)
            return expression
        return expression

    def get_oper_num(self):
        # 生成获取操作数，以及是否生成分数随机判断
        oper_range = self.oper_range
        dec_chance = self.dec_chance  # 遗留问题生成分数的判断decChance放到哪里合适？
        # 将分数出现的概率转换为整形，例：0.5 -> 50
        dec_chance *= 100
        dec_chance = int(dec_chance)

        # 用于存放返回的操作数
        result = {}
        # 若随机生成的100以内的数在概率整形内，则生成分数
        if self.get_random_num(100) <= dec_chance:
            operArray = self.get_range_dec()
            result['oper'] = operArray[0] / operArray[1]
            result['operStr'] = self.dec_to_str(operArray)
            result['operArray'] = [operArray[0], operArray[1]]
        else:
            oper = self.get_random_num(oper_range)
            result['oper'] = oper
            result['operStr'] = str(oper)
            result['operArray'] = [oper, 1]
        return result

    def dec_to_str(self, operArray):
        # 分数转化为字符串  带分数
        operNum1 = operArray[0]
        operNum2 = operArray[1]
        if operNum2 == 1:
            return operNum1
        if (operNum1 > operNum2):
            temp = int(operNum1 / operNum2)
            operNum1 -= (temp * operNum2)
            return str(temp) + "'" + str(operNum1) + "/" + str(operNum2)
        else:
            return str(operNum1) + "/" + str(operNum2)

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

    def get_random_num(self, range): # 获取随机数
        return random.randint(1, range)

    def getOperSymbol(self, operate): # 返回操作符符号
        operSignArray = ['+', '-', '×', '÷']  # 对应operate 1，2，3，4
        return operSignArray[operate - 1]

    def normalize_expression(self, exp_list, e_path):  # exp_list: 表达式列表
        if not exp_list:   # 判断是否存在
            return

        if os.path.exists(e_path):
            with open(e_path, 'r+') as file:
                file.truncate(0)
        for i, exp in enumerate(exp_list):
            exp_str = "Question" + str(i + 1) + ': ' + exp + " =" + "\n"
            with open(e_path, "a+", encoding='utf-8') as f:
                f.write(exp_str)

    def isRepeat(self, express_set, expression):  # express_set: 表达式集合  # expression: 生成的表达式
        suffixExpression = suffix_expression(expression)
        target_exp_suffix = suffixExpression.re  # 后缀表达式列表
        binaryTree = Binary_Tree()
        target_exp_binary_tree = binaryTree.generateBinaryTree(target_exp_suffix)
        for item in express_set:
            suffixExpression2 = suffix_expression(item)
            source_exp_suffix = suffixExpression2.re
            source_exp_binary_tree = binaryTree.generateBinaryTree(source_exp_suffix)
            if binaryTree.isSame(target_exp_binary_tree) == binaryTree.isSame(source_exp_binary_tree):
                return True
        return False

    def calculate(self, expression):  # 计算单一表达式的值
        suffixExpression = suffix_expression(expression)
        exp_value = str(suffixExpression.suffixToValue())
        result = exp_value

        return result
