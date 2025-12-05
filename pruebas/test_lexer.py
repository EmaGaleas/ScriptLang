from core.lexer import Lexer

print("\n========== PRUEBA LEXER 1 (tokens básicos) ==========\n")

codigo = """
set x = "hola"
log x
mkdir carpeta
"""

print("=== Código ===")
print(codigo)

lexer = Lexer(codigo)

try:
    tokens = lexer.tokenize()
    print("\n=== TOKENS ===")
    for t in tokens:
        print(t)
    print("\nLexer procesó el código correctamente")
except SyntaxError as e:
    print("Error léxico detectado:")
    print(e)



print("\n========== PRUEBA LEXER 2 (strings y variables) ==========\n")

codigo2 = """
set saludo = "hola"
set nombre = "mundo"
set mensaje = "${saludo}_${nombre}"
"""

print("=== Código ===")
print(codigo2)

lexer = Lexer(codigo2)

try:
    tokens = lexer.tokenize()
    print("\n=== TOKENS ===")
    for t in tokens:
        print(t)
    print("\nLexer procesó el código correctamente")
except SyntaxError as e:
    print("Error léxico detectado:")
    print(e)
