from core.lexer import Lexer
from core.parser import parse_tokens
from core.semantic import check, SemanticError

# === Código con errores ===
codigo_bad = """
log x
set y = "${z}"
"""

print("\n========== PRUEBA SEMÁNTICA 2 (con errores) ==========\n")
print("=== Código ===")
print(codigo_bad)

lexer = Lexer(codigo_bad)
tokens = lexer.tokenize()

print("\n=== TOKENS ===")
for t in tokens:
    print(t)

ast = parse_tokens(tokens)

print("\n=== AST ===")
print(ast)

print("\n=== SEMÁNTICA ===")
try:
    check(ast)
    print("No se encontraron errores")
except SemanticError as e:
    print("Errores semánticos detectados:")
    print(e)
