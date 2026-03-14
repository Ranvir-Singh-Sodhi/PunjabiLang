import re

KEYWORDS = {
    'manno': 'VAR',
    'likh': 'PRINT',
    'bhar': 'INPUT',
    'je': 'IF',
    'nahi_taan': 'ELSE',
    'jadon_takk': 'WHILE',
    'kamm': 'FUNC',
    'waapas': 'RETURN',
    'shaamil': 'IMPORT',
}

class Token:
    def __init__(self, type, value, line):
        self.type = type
        self.value = value
        self.line = line
        
    def __repr__(self):
        return f"Token({self.type}, '{self.value}', Line {self.line})"

def tokenize(code):
    tokens = []
    current_line = 1
    
    token_specification = [
        ('COMMENT',  r'//.*'),
        ('STRING',   r'".*?"'),         
        ('NUMBER',   r'\d+'),           
        ('WORD',     r'[A-Za-z_]\w*'),  
        ('OP',       r'[+\-*/=<>!]+'),     
        ('PUNC',     r'[(),;{}\[\]:]'),  
        ('NEWLINE',  r'\n'),            
        ('SKIP',     r'[ \t\r]+'),      
        ('MISMATCH', r'.'),             
    ]

    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        
        if kind == 'NEWLINE':
            current_line += 1
            continue
        elif kind == 'SKIP' or kind == 'COMMENT':
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f"Syntax Error: Unexpected character '{value}' at Line {current_line}")
        elif kind == 'WORD':
            kind = KEYWORDS.get(value, 'IDENTIFIER')
            
        tokens.append(Token(kind, value, current_line))
        
    return tokens