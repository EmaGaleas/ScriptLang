from core.lexer import Lexer
from core.parser import parse_tokens

# Código inválido a propósito

print("\n============ PRUEBA 1 ============\n")
codigo = """
set = "hola"
"""

lexer = Lexer(codigo)
tokens = lexer.tokenize()

print("=== TOKENS ===")
for t in tokens:
    print(t)

print("\n=== PARSING ===")
try:
    ast = parse_tokens(tokens)
except SyntaxError as e:
    print("Parser detectó un error sintáctico:")
    print(e)


print("\n============ PRUEBA 2 ============\n")

codigo2 = """
copy "a" "b"
"""

lexer = Lexer(codigo2)
tokens = lexer.tokenize()

print("=== TOKENS ===")
for t in tokens:
    print(t)

print("\n=== PARSING ===")
try:
    ast = parse_tokens(tokens)
except SyntaxError as e:
    print("Parser detectó un error sintáctico:")
    print(e)


print("\n============ PRUEBA 3 ============\n")

codigo3 = """
if "algo" {
    log "x"
}
"""

lexer = Lexer(codigo3)
tokens = lexer.tokenize()

print("=== TOKENS ===")
for t in tokens:
    print(t)

print("\n=== PARSING ===")
try:
    ast = parse_tokens(tokens)
except SyntaxError as e:
    print("Parser detectó un error sintáctico:")
    print(e)