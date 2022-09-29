import os
import re
from Expression import suffix_expression


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