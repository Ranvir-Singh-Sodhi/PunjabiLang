from src.ast import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def peek(self):
        if self.current < len(self.tokens):
            return self.tokens[self.current]
        return None

    def consume(self, expected_type=None):
        token = self.peek()
        if not token:
            last_line = self.tokens[-1].line if self.tokens else 1
            raise SyntaxError(f"Line {last_line}: Expected {expected_type} but reached end of file.")
            
        if expected_type and token.type != expected_type:
            raise SyntaxError(f"Line {token.line}: Expected {expected_type}, but got {token.type} ('{token.value}')")
        
        self.current += 1
        return token

    def parse(self):
        statements = []
        while self.peek() is not None:
            statements.append(self.parse_statement())
        return Program(statements)

    def parse_statement(self):
        token = self.peek()
        if token.type == 'IMPORT': return self.parse_import_stmt()
        elif token.type == 'VAR': return self.parse_var_decl()
        elif token.type == 'PRINT': return self.parse_print_stmt()
        elif token.type == 'IF': return self.parse_if_stmt()
        elif token.type == 'WHILE': return self.parse_while_stmt()
        elif token.type == 'FUNC': return self.parse_func_def()
        elif token.type == 'RETURN': return self.parse_return_stmt()
        elif token.type == 'IDENTIFIER':
            if len(self.tokens) > self.current + 1 and self.tokens[self.current + 1].value == '(':
                expr = self.parse_primary()
                if self.peek() and self.peek().value == ';':
                    self.consume('PUNC')
                return expr
            return self.parse_assign_stmt()
        else: 
            raise SyntaxError(f"Line {token.line}: Unexpected command '{token.value}'")

    def parse_import_stmt(self):
        self.consume('IMPORT')
        path_token = self.consume('STRING')
        self.consume('PUNC')
        return ImportStmt(path_token.value[1:-1])
        
    def parse_while_stmt(self):
        self.consume('WHILE')
        self.consume('PUNC')
        condition = self.parse_expression()
        self.consume('PUNC')
        self.consume('PUNC')
        body = []
        while self.peek() and self.peek().value != '}':
            body.append(self.parse_statement())
        self.consume('PUNC')
        return WhileStmt(condition, body)

    def parse_assign_stmt(self):
        target = self.parse_primary()
        self.consume('OP')
        value = self.parse_expression()
        self.consume('PUNC')
        return ComplexAssignStmt(target, value)
    
    def parse_func_def(self):
        self.consume('FUNC')
        name = self.consume('IDENTIFIER').value
        self.consume('PUNC')
        params = []
        if self.peek() and self.peek().value != ')':
            params.append(self.consume('IDENTIFIER').value)
            while self.peek() and self.peek().value == ',':
                self.consume('PUNC')
                params.append(self.consume('IDENTIFIER').value)
        self.consume('PUNC')
        self.consume('PUNC')
        body = []
        while self.peek() and self.peek().value != '}':
            body.append(self.parse_statement())
        self.consume('PUNC')
        return FunctionDef(name, params, body)

    def parse_return_stmt(self):
        self.consume('RETURN')
        value = self.parse_expression()
        self.consume('PUNC')
        return ReturnStmt(value)

    def parse_if_stmt(self):
        self.consume('IF')
        self.consume('PUNC')
        condition = self.parse_expression()
        self.consume('PUNC')
        self.consume('PUNC')
        then_branch = []
        while self.peek() and self.peek().value != '}':
            then_branch.append(self.parse_statement())
        self.consume('PUNC')
        else_branch = None
        if self.peek() and self.peek().type == 'ELSE':
            self.consume('ELSE')
            self.consume('PUNC')
            else_branch = []
            while self.peek() and self.peek().value != '}':
                else_branch.append(self.parse_statement())
            self.consume('PUNC')
        return IfStmt(condition, then_branch, else_branch)

    def parse_var_decl(self):
        self.consume('VAR')
        name = self.consume('IDENTIFIER')
        self.consume('OP')
        value = self.parse_expression()
        self.consume('PUNC')
        return VarDecl(name.value, value)

    def parse_print_stmt(self):
        self.consume('PRINT')
        self.consume('PUNC')
        expr = self.parse_expression()
        self.consume('PUNC')
        self.consume('PUNC')
        return PrintStmt(expr)

    def parse_expression(self):
        left = self.parse_primary()
        token = self.peek()
        while token and token.type == 'OP' and token.value != '=':
            operator = self.consume('OP').value
            right = self.parse_primary()
            left = BinaryExpr(left, operator, right)
            token = self.peek()
        return left

    def parse_primary(self):
        token = self.consume()
        expr = None
        
        if token.type == 'NUMBER':
            expr = NumberLiteral(int(token.value))
        elif token.type == 'STRING':
            expr = StringLiteral(token.value[1:-1])
        elif token.type == 'INPUT':
            self.consume('PUNC'); self.consume('PUNC')
            expr = InputExpr()
        elif token.type == 'PUNC' and token.value == '(':
            expr = self.parse_expression()
            self.consume('PUNC')
        elif token.type == 'PUNC' and token.value == '{':
            pairs = {}
            if self.peek() and self.peek().value != '}':
                key = self.parse_expression()
                self.consume('PUNC')
                val = self.parse_expression()
                pairs[key] = val
                while self.peek() and self.peek().value == ',':
                    self.consume('PUNC')
                    key = self.parse_expression()
                    self.consume('PUNC')
                    val = self.parse_expression()
                    pairs[key] = val
            self.consume('PUNC')
            expr = DictLiteral(pairs)
        elif token.type == 'IDENTIFIER':
            if self.peek() and self.peek().value == '(':
                self.consume('PUNC')
                args = []
                if self.peek() and self.peek().value != ')':
                    args.append(self.parse_expression())
                    while self.peek() and self.peek().value == ',':
                        self.consume('PUNC')
                        args.append(self.parse_expression())
                self.consume('PUNC')
                expr = FunctionCall(token.value, args)
            else:
                expr = Identifier(token.value)
        elif token.type == 'PUNC' and token.value == '[':
            elements = []
            if self.peek() and self.peek().value != ']':
                elements.append(self.parse_expression())
                while self.peek() and self.peek().value == ',':
                    self.consume('PUNC')
                    elements.append(self.parse_expression())
            self.consume('PUNC')
            expr = ArrayLiteral(elements)
        else:
            raise SyntaxError(f"Line {token.line}: Invalid expression: {token.value}")

        while self.peek() and self.peek().value == '[':
            self.consume('PUNC')
            index = self.parse_expression()
            self.consume('PUNC')
            expr = IndexExpr(expr, index)

        return expr