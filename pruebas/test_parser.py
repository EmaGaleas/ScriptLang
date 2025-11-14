from core.lexer import Lexer
from core.parser import parse_tokens

codigo = """
set mensaje = "hola"
log "probando"
"""

print("=== Código ===")
print(codigo)

# --- Lexing ---
lexer = Lexer(codigo)
tokens = lexer.tokenize()

print("\n=== TOKENS ===")
for t in tokens:
    print(t)

# --- Parsing ---
ast = parse_tokens(tokens)

print("\n=== AST ===")
print(ast)
print("\n=== Statements ===")
for s in ast.statements:
    print(s)
