from core.lexer import Lexer

print("\n========== PRUEBA LEXER ERROR 1 (string sin cerrar) ==========\n")

codigo = """
set x = "Hola
"""

print("=== Código ===")
print(codigo)

lexer = Lexer(codigo)

try:
    tokens = lexer.tokenize()
    print("ERROR: El lexer NO detectó el string sin cerrar")
except SyntaxError as e:
    print("Error léxico detectado correctamente:")
    print(e)



print("\n========== PRUEBA LEXER ERROR 2 (caracter ilegal) ==========\n")

codigo2 = """
set x = "hola"
$%^&  # caracteres inválidos
"""

print("=== Código ===")
print(codigo2)

lexer = Lexer(codigo2)

try:
    tokens = lexer.tokenize()
    print("ERROR: El lexer NO detectó los caracteres ilegales")
except SyntaxError as e:
    print("Error léxico detectado correctamente:")
    print(e)
