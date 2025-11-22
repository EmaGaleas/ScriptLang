# pruebas/manual_test_all.py

import sys
from core.lexer import Lexer
from core.parser import parse_tokens
from core.interpreter import execute, InterpreterError
from biblioteca import filesystem, logger
from pathlib import Path

# Inicializa logger
logger.init_logger("test_interpreter.log", level="DEBUG")

# Función helper para correr un script
def run_script(src):    
    print(f"=== Ejecutando script ===\n{src}\n")
    try:
        tokens = Lexer(src).tokenize()
        ast = parse_tokens(tokens)
        interp = execute(ast)
        print("=> OK\n")
    except InterpreterError as e:
        print(f"=> ERROR de ejecución: {e}\n")
    except SyntaxError as e:
        print(f"=> ERROR de sintaxis: {e}\n")
    except Exception as e:
        print(f"=> ERROR inesperado: {e}\n")


# casos

# 1Variables e interpolación
script1 = '''
set nombre = "Ema"
log "Hola ${nombre}"
'''
run_script(script1)

# Crear y borrar directorios
script2 = '''
makedir "carpeta_prueba"
log "Directorio creado"
delete "carpeta_prueba"
log "Directorio borrado"
'''
run_script(script2)

# Crear archivo simulado usando filesystem, luego copy y move
tmp_file = Path("archivo_test.txt")
tmp_file.write_text("hola")  # Crear archivo directo sin run

script3 = f'''
copy "{tmp_file}" to "copia.txt"
log "Archivo copiado"
move "copia.txt" to "copia2.txt"
log "Archivo movido"
delete "{tmp_file}"
delete "copia2.txt"
log "Archivos borrados"
'''
run_script(script3)

# If exists
tmp_file2 = Path("archivo_if.txt")
tmp_file2.write_text("x")

script4 = f'''
if exists "{tmp_file2}" {{
    log "Archivo existe"
}} else {{
    log "Archivo NO existe"
}}
delete "{tmp_file2}"
'''
run_script(script4)

# Variable inexistente
script5 = '''
log "Variable no definida: ${NO_EXISTE}"
'''
run_script(script5)

# Errores de sintaxis
script6 = 'log "cadena sin cerrar\n'
run_script(script6)

script7 = 'set = "x"\n'
run_script(script7)

print("\n=== Pruebas completadas. Revisa manual_test_all.log para detalles de logs ===")
