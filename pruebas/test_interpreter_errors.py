from core.lexer import Lexer
from core.parser import parse_tokens
from core.semantic import check
from core.interpreter import execute, InterpreterError


print("\n========== PRUEBA INTERPRETER ERROR 1 (variable no existe) ==========\n")

codigo = """
log x
"""

print("=== Código ===")
print(codigo)

lexer = Lexer(codigo)
tokens = lexer.tokenize()
ast = parse_tokens(tokens)

print("\n=== SEMÁNTICA ===")
try:
    check(ast)
    print("ERROR: la semántica debería fallar")
except Exception as e:
    print("Error semántico detectado:")
    print(e)



print("\n========== PRUEBA INTERPRETER ERROR 2 (directorio no existe) ==========\n")

codigo2 = """
copy "no_existe.txt" to "destino.txt"
"""

print("=== Código ===")
print(codigo2)

lexer = Lexer(codigo2)
tokens = lexer.tokenize()
ast = parse_tokens(tokens)

print("\n=== SEMÁNTICA ===")
try:
    check(ast)
    print("Sin errores semánticos (correcto)")
except Exception as e:
    print("La semántica no debería fallar aquí")
    print(e)

print("\n=== INTERPRETACIÓN ===")
try:
    execute(ast)
    print("ERROR: debería fallar al ejecutar (archivo no existe)")
except InterpreterError as e:
    print("Error de ejecución detectado:")
    print(e)
