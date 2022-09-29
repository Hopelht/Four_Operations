import os
from Expression import suffix_expression


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

