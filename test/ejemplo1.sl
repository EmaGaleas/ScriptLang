log "=== Inicio del script de respaldo ==="

# Variables
set base = "test"
set origen = "${base}/datos"
set destino = "${base}/backup"
set archivo = "${origen}/archivo1.txt"

# Crear estructura base
if exists "${base}" {
    log "La carpeta base ya existe"
} else {
    log "Creando carpeta base"
    makedir "${base}"
}

# Crear carpeta de datos
if exists "${origen}" {
    log "La carpeta de datos ya existe"
} else {
    log "Creando carpeta de datos"
    makedir "${origen}"
}

# Crear carpeta de respaldo
if exists "${destino}" {
    log "La carpeta de respaldo ya existe"
} else {
    log "Creando carpeta de respaldo"
    makedir "${destino}"
}

# Verificar archivo y copiarlo
if exists "${archivo}" {
    log "Archivo encontrado, copiando a respaldo"
    copy "${archivo}" to "${destino}/archivo1.txt"
    delete "${archivo}"
} else {
    log "No hay archivo para respaldar"
}

log "=== Fin del script de respaldo ==="
