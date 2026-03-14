import random
import os
from datetime import datetime
from src.ast import *

class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

class Evaluator:
    def __init__(self, environment):
        self.env = environment

    def evaluate(self, node):
        if isinstance(node, Program):
            for stmt in node.statements:
                self.evaluate(stmt)
                
        elif isinstance(node, ImportStmt):
            from src.lexer import tokenize
            from src.parser import Parser
            file_path = node.file_path
            search_paths = [file_path, os.path.join("examples", file_path)]
            found_path = None
            for p in search_paths:
                if os.path.exists(p):
                    found_path = p
                    break
            if not found_path:
                raise Exception(f"Error: File '{file_path}' nahi labhi.")
            with open(found_path, 'r', encoding='utf-8') as f:
                code = f.read()
            ext_tokens = tokenize(code)
            ext_parser = Parser(ext_tokens)
            ext_ast = ext_parser.parse()
            self.evaluate(ext_ast)
            return None

        elif isinstance(node, VarDecl):
            self.env.set(node.name, self.evaluate(node.value))
            
        elif isinstance(node, PrintStmt):
            print(self.evaluate(node.expression))
            
        elif isinstance(node, NumberLiteral) or isinstance(node, StringLiteral):
            return node.value
            
        elif isinstance(node, Identifier):
            return self.env.get(node.name)
        
        elif isinstance(node, BinaryExpr):
            left = self.evaluate(node.left)
            right = self.evaluate(node.right)
            if node.operator == '+':
                if isinstance(left, str) or isinstance(right, str):
                    return str(left) + str(right)
                return left + right
            elif node.operator == '-': return left - right
            elif node.operator == '*': return left * right
            elif node.operator == '/': return left / right
            elif node.operator == '>': return left > right
            elif node.operator == '<': return left < right
            elif node.operator == '==': return left == right
            
        elif isinstance(node, IfStmt):
            if self.evaluate(node.condition):
                for stmt in node.then_branch: self.evaluate(stmt)
            elif node.else_branch:
                for stmt in node.else_branch: self.evaluate(stmt)
            
        elif isinstance(node, InputExpr):
            return input("> ")
        
        elif isinstance(node, ComplexAssignStmt):
            val = self.evaluate(node.value)
            if isinstance(node.target, Identifier):
                self.env.set(node.target.name, val)
            elif isinstance(node.target, IndexExpr):
                obj = self.evaluate(node.target.collection)
                idx = self.evaluate(node.target.index)
                obj[idx] = val

        elif isinstance(node, WhileStmt):
            while self.evaluate(node.condition):
                for stmt in node.body: self.evaluate(stmt)

        elif isinstance(node, FunctionDef):
            self.env.set(node.name, node)

        elif isinstance(node, ReturnStmt):
            raise ReturnException(self.evaluate(node.value))
        
        elif isinstance(node, ArrayLiteral):
            return [self.evaluate(e) for e in node.elements]

        elif isinstance(node, IndexExpr):
            c = self.evaluate(node.collection)
            i = self.evaluate(node.index)
            return c[i]

        elif isinstance(node, DictLiteral):
            return {self.evaluate(k): self.evaluate(v) for k, v in node.pairs.items()}
        
        elif isinstance(node, FunctionCall):
            if node.name == 'ganit': return len(self.evaluate(node.args[0]))
            elif node.name == 'ank': return int(self.evaluate(node.args[0]))
            elif node.name == 'tuka': return random.randint(self.evaluate(node.args[0]), self.evaluate(node.args[1]))
            elif node.name == 'samaa': return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            elif node.name == 'kholo': return open(self.evaluate(node.args[0]), self.evaluate(node.args[1]), encoding='utf-8')
            elif node.name == 'parho': return self.evaluate(node.args[0]).read()
            elif node.name == 'likho_file': 
                self.evaluate(node.args[0]).write(str(self.evaluate(node.args[1])))
                return None
            elif node.name == 'band_karo': 
                self.evaluate(node.args[0]).close()
                return None
            else:
                f = self.env.get(node.name)
                from src.environment import Environment
                lenv = Environment(parent=self.env)
                for i, p in enumerate(f.params): lenv.set(p, self.evaluate(node.args[i]))
                evaltr = Evaluator(lenv)
                try:
                    for s in f.body: evaltr.evaluate(s)
                except ReturnException as r: return r.value
            return None
        else:
            raise Exception(f"Unknown Node: {type(node).__name__}")