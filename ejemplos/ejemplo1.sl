# Ejemplo de ScriptLang

set name = "Ema"
copy "data.txt" to "backup/data.txt"

if exists "backup/data.txt" {
    log "Archivo copiado exitosamente!"
} else {
    log "Error: no se pudo copiar el archivo."
}

run "cleanup.sh"
