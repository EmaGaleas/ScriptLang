from core.lexer import Lexer
from core.parser import parse_tokens
from core.semantic import check
from core.interpreter import execute, InterpreterError
from biblioteca import filesystem, logger


print("\n========== PRUEBA INTERPRETER 1 (operaciones básicas) ==========\n")

codigo = """
set x = "hola"
set y = "${x}_mundo"
log y
"""

print("=== Código ===")
print(codigo)

# LEXER
lexer = Lexer(codigo)
tokens = lexer.tokenize()

print("\n=== TOKENS ===")
for t in tokens:
    print(t)

# PARSER
ast = parse_tokens(tokens)

print("\n=== AST ===")
print(ast)

# SEMÁNTICA
print("\n=== SEMÁNTICA ===")
check(ast)
print("Sin errores semánticos")

# INTERPRETER
print("\n=== INTERPRETACIÓN ===")
try:
    execute(ast)
    print("Script ejecutado correctamente")
except InterpreterError as e:
    print("ERROR en ejecución:")
    print(e)
