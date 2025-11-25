
import sys
from core.lexer import Lexer
from core.parser import parse_tokens
from core.interpreter import execute, InterpreterError
from core.semantic import SemanticError


def run_script_text(src: str) -> int:
	try:
		tokens = Lexer(src).tokenize()
		ast = parse_tokens(tokens)
		# semantic.check se llama dentro de execute (punto de integración)
		execute(ast)
		return 0
	except SyntaxError as e:
		print(f"[Sintaxis] {e}", file=sys.stderr)
		return 2
	except SemanticError as e:
		print(f"[Semántico] {e}", file=sys.stderr)
		return 3
	except InterpreterError as e:
		print(f"[Ejecución] {e}", file=sys.stderr)
		return 4
	except Exception as e:
		print(f"[Error inesperado] {e}", file=sys.stderr)
		return 5


def main(argv=None):
	argv = argv or sys.argv[1:]
	if len(argv) >= 1:
		path = argv[0]
		with open(path, 'r', encoding='utf-8') as f:
			src = f.read()
	else:
		print('Leyendo script desde stdin. Termina con EOF (Ctrl+D / Ctrl+Z).')
		src = sys.stdin.read()

	return run_script_text(src)


if __name__ == '__main__':
	sys.exit(main())

