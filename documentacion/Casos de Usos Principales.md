# Casos de Usos Principales

A continuación se documentan los patrones sintácticos esenciales que ScriptLang utiliza para la automatización de tareas del sistema, ilustrados con ejemplos de código válidos.



1. ##### Ejecutar Comandos Nativos (run)



El comando **run** permite a ScriptLang interactuar directamente con la shell del sistema operativo para ejecutar comandos que no son nativos del lenguaje.



**Sintaxis**: run "comando <argumentos>"

**Ejemplo**: run "ls -l"

**Uso de variables:** set dir = "documentos"; run "ls -l $dir"



##### 2\. Crear Archivos y Directorios



La creación se maneja principalmente a nivel de directorios con **makedir**. La creación de archivos vacíos se realiza indirectamente con run.



**Crear Directorio:**

comando: makedir "ruta/carpeta"	

ejemplo: makedir "backups/temp"



**Crear Archivo Vacío:**

comando: run "touch ruta/archivo"

ejemplo: run "touch backup/archivo.txt"



##### 3\. Verificar Existencia de un Archivos



ScriptLang no puede leer contenido de archivos en variables, pero sí verificar la existencia de una ruta, útil para condicionales de automatización.



**Verificar Existencia:**

comando: if exists "ruta" { <bloque> }

ejemplo: if exists "backup/archivo.txt" { log "Archivo encontrado" }



**Verificar con else:**

comando: if exists "ruta" { ... } else { ... }

ejemplo: if exists "backup/archivo.txt" 

&nbsp;			{ delete "backup/archivo.txt"} else { 

&nbsp;			log "No fue encontrado" }



##### 4\. Escribir Archivos (Mover, Copiar y Log)



Estas operaciones implican manipulación de datos en disco **(copy, move)** o registro de mensajes de estado **(log)**.



**Mover Archivo:**

comando: move

sintaxis general: move "origen" to "destino"

ejemplo: move "archivo.txt" to "backup/archivo.txt"



**Copiar Archivo:**

comando: copy

sintaxis: copy "origen" to "destino"

ejemplo: copy "datos.txt" to "backup/datos.txt"



**Registrar Log:**

comando: log

sintaxis: log "mensaje"

ejemplo: log "Proceso finalizado"



##### 5\. Borrar Archivos (delete)

Esta operación **borra** el archivo indicado y registra la acción el log



comando: delete

sintaxis: delete "ruta/archivo"

ejemplo: delete "backup/archivo.txt"



##### Ejemplo completo de un script .sl

\# ======= **Definir variables** ========== 



set archivo\_origen = "notas.txt"

set carpeta\_backup = "backup"

set carpeta\_final = "final"

set temp = "temp/archivo\_temp.txt"



\# ======= **Crear** carpetas si no existen =======



if exists "$carpeta\_backup" {

&nbsp;   log "Carpeta $carpeta\_backup si existe"

} else {

&nbsp;   makedir "$carpeta\_backup"

&nbsp;   log "Carpeta $carpeta\_backup fue creada ya que no existía"

}



if exists "$carpeta\_final" {

&nbsp;   log "Carpeta $carpeta\_final si existe"

} else {

&nbsp;   makedir "$carpeta\_final"

&nbsp;   log "Carpeta $carpeta\_final fue creada ya que no existía"

}



\# === **Verificar existencia** de archivo temporal y **eliminarlo** si existe =====



if exists "$temp" {

&nbsp;   delete "$temp"

&nbsp;   log "Archivo temporal $temp fue eliminado"

} else {

&nbsp;   log "No existen archivos temporales"

}



\# === **Verificar existencia** del archivo principal =====



if exists "$archivo\_origen" {

&nbsp;   log "Archivo $archivo\_origen fue encontrado. Iniciando proceso..."



&nbsp;   # === **Copiar** archivo a la carpeta de backup ======

&nbsp;   copy "$archivo\_origen" to "$carpeta\_backup/$archivo\_origen"

&nbsp;   log "Archivo $archivo\_origen fue copiado a $carpeta\_backup"



&nbsp;   # === **Mover** archivo a carpeta final =====

&nbsp;   move "$archivo\_origen" to "$carpeta\_final/$archivo\_origen"

&nbsp;   log "Archivo $archivo\_origen fue movido a $carpeta\_final"



&nbsp;   # === **Ejecutar comando externo (ejemplo de limpieza)** =======

&nbsp;   run "echo Limpieza completada"

&nbsp;   log "Comando de limpieza ejecutado"



} else {

&nbsp;   # === Caso de archivo no encontrado ===

&nbsp;   log "ERROR: El archivo $archivo\_origen no existe"

}





