############################################
# ERRORES LÉXICOS
############################################

# Caracter ilegal
set mensaje = "hola" @

# Cadena sin cerrar
set archivo = "ruta/sin/cerrar

############################################
# ERRORES SINTÁCTICOS
############################################

# Falta '=' en asignación
set saludo  "hola"

# Comando mal formado: falta 'to'
copy "origen.txt" "destino.txt"

# If sin exists
if "archivo.txt" {
    log "Debería fallar"
}

# Bloque if sin cerrar
if exists "/tmp/a" {
    log "faltó cerrar"

############################################
# ERRORES "SEMÁNTICOS" (control de uso)
############################################

# Variable usada sin haber sido definida antes (no fatal pero muestra comportamiento)
log $no_definida

# Variable mal declarada (identificador inválido)
set 123var = "hola"

# Palabra clave mal usada
run "programa" to "otro/lugar"

