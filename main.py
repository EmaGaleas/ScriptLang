import sys
from core.lexer import Lexer
from core.parser import parse_tokens
from core.interpreter import execute, InterpreterError
from biblioteca import logger
from biblioteca.filesystem import read_file

# Inicializar logger
logger.init_logger("scriptlang.log", level="INFO")

def run_script(path: str):
    try:
        # 1. Leer archivo
        script_text = read_file(path)

        # 2. Lexer
        lexer = Lexer(script_text)
        tokens = lexer.tokenize()

        # 3. Parser
        ast = parse_tokens(tokens)

        # 4. Ejecutar usando la función helper de tu intérprete
        execute(ast)

    except FileNotFoundError:
        print(f"Error: No se pudo leer el archivo '{path}'.")
        logger.log_error(f"No se pudo leer el archivo: {path}")

    except InterpreterError as e:
        print(f"Error de ejecución: {e}")
        logger.log_error(f"Error de ejecución: {e}")

    except Exception as e:
        print(f"Error inesperado: {e}")
        logger.log_error("Error inesperado", exc_info=True)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python main.py <script.sl>")
        sys.exit(1)

    run_script(sys.argv[1])
