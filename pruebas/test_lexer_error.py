from core.lexer import Lexer

def main():
    ruta = "ejemplos/errores.sl"   # <-- Cambia el archivo aquí

    with open(ruta, "r", encoding="utf-8") as f:
        codigo = f.read()

    print("=== Código ===\n")
    print(codigo)
    print("\n=== TOKENS ===")

    try:
        lexer = Lexer(codigo)
        tokens = lexer.tokenize()
        for t in tokens:
            print(t)

    except SyntaxError as e:
        print("\n--- ERROR EN LÉXICO ---")
        print(e)

if __name__ == "__main__":
    main()
