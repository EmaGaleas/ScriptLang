#!/usr/bin/env python3
import sys
import os

from core.lexer import Lexer
from core.parser import parse_tokens
from core.semantic import SemanticError
from core.interpreter import execute, InterpreterError


def run_script_text(src: str) -> int:
    """Ejecuta código ScriptLang proveniente de un string completo."""
    try:
        # 1. Lexing
        tokens = Lexer(src).tokenize()

        # 2. Parsing
        ast = parse_tokens(tokens)

        # 3 y 4. Análisis semántico + ejecución
        execute(ast)

        return 0  # Ejecución correcta

    except SyntaxError as e:
        print(f"[Error de Sintaxis] {e}", file=sys.stderr)
        return 2
    except SemanticError as e:
        print(f"[Error Semántico] {e}", file=sys.stderr)
        return 3
    except InterpreterError as e:
        print(f"[Error en Ejecución] {e}", file=sys.stderr)
        return 4
    except Exception as e:
        print(f"[Error inesperado] {e}", file=sys.stderr)
        return 5


def main(argv=None):
    """Punto de entrada de la herramienta ScriptLang."""
    argv = argv or sys.argv[1:]

    if len(argv) == 0 or argv[0] in ("-h", "--help"):
        print("Uso:")
        print("   python main.py archivo.sl")
        print()
        print("Si no se especifica archivo, el script se leerá desde stdin.")
        return 1

    # --- Si se especifica archivo ---
    path = argv[0]

    if not os.path.exists(path):
        print(f"[Archivo no encontrado] {path}", file=sys.stderr)
        return 6

    try:
        with open(path, "r", encoding="utf-8") as f:
            src = f.read()
    except Exception as e:
        print(f"[Error al leer archivo] {e}", file=sys.stderr)
        return 7

    return run_script_text(src)


if __name__ == "__main__":
    sys.exit(main())
