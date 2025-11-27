# Ejemplo de ScriptLang

set name = "Juana"
copy "ejemplo1.txt" to "Lenguajes/ejemplos/ejemplo1"

if exists "Lenguajes/ejemplos/ejemplo1" {
    log "Archivo copiado exitosamente :l"
} else {
    log "Error: no se pudo copiar el archivo :/"
}

run "cleanup.sh"
