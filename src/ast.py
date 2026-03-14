class Node:
    pass

class Program(Node):
    def __init__(self, statements):
        self.statements = statements

class VarDecl(Node):
    def __init__(self, name, value):
        self.name = name
        self.value = value

class PrintStmt(Node):
    def __init__(self, expression):
        self.expression = expression

class NumberLiteral(Node):
    def __init__(self, value):
        self.value = value

class Identifier(Node):
    def __init__(self, name):
        self.name = name

class StringLiteral(Node):
    def __init__(self, value):
        self.value = value

class InputExpr(Node):
    pass

class BinaryExpr(Node):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class IfStmt(Node):
    def __init__(self, condition, then_branch, else_branch=None):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

class WhileStmt(Node):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class AssignStmt(Node):
    def __init__(self, name, value):
        self.name = name
        self.value = value

class ComplexAssignStmt(Node):
    def __init__(self, target, value):
        self.target = target
        self.value = value

class FunctionDef(Node):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

class FunctionCall(Node):
    def __init__(self, name, args):
        self.name = name
        self.args = args

class ReturnStmt(Node):
    def __init__(self, value):
        self.value = value

class ArrayLiteral(Node):
    def __init__(self, elements):
        self.elements = elements

class IndexExpr(Node):
    def __init__(self, collection, index):
        self.collection = collection
        self.index = index

class DictLiteral(Node):
    def __init__(self, pairs):
        self.pairs = pairs

class ImportStmt(Node):
    def __init__(self, file_path):
        self.file_path = file_path