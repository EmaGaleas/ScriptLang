# Ejemplos de uso de ScriptLang

Este documento contiene ejemplos básicos y pruebas relacionadas con el intérprete de ScriptLang, enfocados inicialmente en el **Lexer**, que es la primera fase del proceso de análisis de un script `.sl`.

---

## Prueba del Lexer

El archivo de prueba para el Lexer se encuentra ubicado en `pruebas/test_lexer.py `

Este archivo contiene pruebas unitarias escritas con `unittest`, cuyo objetivo es validar que el analizador léxico (Lexer) sea capaz de:

- Detectar palabras clave del lenguaje (`set`, `copy`, `if`, `log`, etc.).
- Reconocer variables (`VAR`).
- Leer correctamente cadenas entre comillas dobles (`"texto"`).
- Identificar símbolos como `=`, `{`, `}`, `$`, etc.
- Ignorar comentarios (`# comentario`).
- Asegurar que se genera un token final de fin de archivo (`END`).

### Contenido del archivo de prueba (`test_lexer.py`)

Incluye pruebas para:

- Un script básico con asignación y copia de archivos.
- Un bloque `if-else` que verifica la existencia de un archivo y muestra un log.

---

## Ejemplo de script `.sl`

El primer ejemplo de script funcional se encuentra en `ejemplos/ejemplo1.sl`

Su contenido demuestra conceptos clave como:

- Asignación con `set`
- Copia de archivos con `copy`
- Control condicional con `if exists`
- Ejecución de comandos externos con `run`
- Manejo y registro de mensajes con `log`

---

## Cómo ejecutar las pruebas del Lexer

Para ejecutar las pruebas unitarias del Lexer, abre una terminal en la carpeta raíz del proyecto (`ScriptLang/`) y ejecuta el siguiente comando:

```bash
python -m unittest discover -s pruebas
```
**Salida esperada**
si el Lexer se comporta correctamente, debería ser:
```
----------------------------------------------------------------------
Ran 2 tests in 0.002s

OK
```
---
## --🐛🐛🐛🐛🐛🐛🐛🐛 Depuración para ver tokens generados🐛🐛🐛🐛🐛🐛🐛🐛-- 

Existe también un script opcional de depuración llamado: `debug_lexer.py`
Este archivo se encuentra directamente en la carpeta raíz del proyecto (`ScriptLang/`) y permite imprimir en consola todos los tokens generados por el Lexer para un archivo específico, se ejecuta mediante el siguiente comando:

```bash
python debug_lexer.py
```
Este comando mostrará uno por uno todos los `Token(type, value, line, colum)` generados por el Lexer al analizar el archivo `ejemplos/ejemplo1.sl`. Cabe mencionar que `se borrará` en un futuro próximo.

---
## Este documento crecerá 
A medida que se añadan nuevas características al lenguaje, se añadiran nuevos ejemplos, como:

- Ejecución del intérprete completo
- Pruebas del parser y analizador semántico
- Ejemplos avanzados con variables, logs y automatización real de tareas del sistema
