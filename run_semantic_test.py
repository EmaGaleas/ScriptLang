from core.lexer import Lexer
from core.parser import parse_tokens
from core.interpreter import execute
from core.semantic import SemanticError

# Script que usa una variable no declarada en interpolación
src = 'log "Hola ${NO_EXISTE}"\n'

print('Tokens -> AST -> semantic.check -> execute')
try:
    tokens = Lexer(src).tokenize()
    ast = parse_tokens(tokens)
    # execute() ahora ejecuta semantic.check internamente
    execute(ast)
    print('EJECUTADO: no se detectó error semántico (unexpected)')
except SemanticError as e:
    print('SEMANTIC ERROR DETECTADO:')
    print(e)
except Exception as e:
    print('OTRO ERROR:')
    print(type(e), e)
