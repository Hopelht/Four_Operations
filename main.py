# -*- codeing = utf-8 -*-
# @Time : 2022/9/25 20：00
# @Author : 丁冠智、钟华峥
# @File : main.py
# @Software : PyCharm

import re
import sys
from Answer import Answer
from Question import Question
import argparse
import os


def main():
    # 确保输入符合命令行要求
    command = ''
    for index in range(1, len(sys.argv)):
        command += sys.argv[index]
    num_mode = '-n([\d]+)'  # 正则表达式模式
    value_mode = '-r([\d]+)'
    need = int(re.search(num_mode, command).group(1))  # -n的参数
    erange = int(re.search(value_mode, command).group(1))  # -r的参数
    if (len(sys.argv) != 9) or (need <= 0) or (erange <= 0):  # 正确输入的话，会有9个参数，['main.py', '-n', '10', '-r', '10', '-_path', 'Exercises.txt', '-a', 'Answer.txt']
        print("请按照格式输入正确的命令行：如python main.py -n 10 -r 10 -e Exercises.txt -a Answer.txt")
        exit(1)

    # 输入文件绝对路径，-e为要问题文件，-a为答案文件
    parser = argparse.ArgumentParser(description="小学四则运算题目生成器")
    parser.add_argument('-n', type=str, help='生成题目的数量')
    parser.add_argument('-r', type=str, default=0, help='题目中数值（自然数、真分数和真分数分母）的范围')
    parser.add_argument('-e', type=str, default=" ", help='生成题目文件的路径')
    parser.add_argument('-a', type=str, default=" ", help='生成答案文件的路径')

    # 处理命令行
    args = parser.parse_args()
    n = int(args.n)
    r = int(args.r)
    e_path = args.e
    e_path = e_path.strip()
    a_path = args.a
    a_path = a_path.strip()


    # 生成问题
    _question = Question(n, r, e_path)
    questions = _question.problem_array
    for index, _questions in enumerate(questions):
        print(f"question {index + 1}:", questions[index])

    # 存储答案
    answer = Answer(a_path)
    answer.expression_result(questions)  # 生成题目的答案


if __name__ == '__main__':
    main()
