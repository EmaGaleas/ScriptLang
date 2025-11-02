# debug_lexer.py
from core.lexer import Lexer

with open("ejemplos/ejemplo1.sl", "r") as f:
    código = f.read()

lexer = Lexer(código)
tokens = lexer.tokenize()
for token in tokens:
    print(token)