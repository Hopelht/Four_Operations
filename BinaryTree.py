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
