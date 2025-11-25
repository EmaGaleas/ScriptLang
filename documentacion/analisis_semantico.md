**Análisis Semántico**

- **Ubicación:** `core/semantic.py`
- **Propósito:** detectar errores en el AST sin ejecutar el programa, prevenir acciones peligrosas (p. ej. borrar archivos) y proporcionar mensajes claros al usuario antes de que el intérprete realice operaciones de E/S o sistema.

**Flujo integrado**

- `src` → `core/lexer.py` → `core/parser.py` → `core/ast_nodes.py` (AST) → `core/semantic.check(ast)` → `core/interpreter.execute(ast)`
- `core/interpreter.execute()` llama internamente a `semantic.check()` y aborta con `SemanticError` si hay problemas.

Principales reglas implementadas

- Variables:
  - Las referencias directas (`VariableRefNode`) deben estar definidas (debe existir una `set var = "..."` previa).
  - Interpolación en strings (`"Hola ${VAR}"`) requiere que `VAR` esté definida; si no, se lanza `SemanticError` con localización.

- Propagación simple de constantes:
  - Si la asignación es literal (`set x = "ruta"`), el analizador registra `x` como constante y usa ese valor cuando `x` aparece en comandos (p. ej. `copy x to "d"`).
  - Esto permite comprobar existencia de archivos si el valor es una cadena literal conocida en tiempo de análisis.

- Comandos de archivos y seguridad:
  - `copy`/`move`: se validan las expresiones (variables/strings). Si el origen es literal o una variable propagada a literal, se verifica que el origen exista (solo lectura, usando `biblioteca.filesystem.exists`). Si el destino es literal conocido, se valida que el directorio padre exista.
  - `delete`: si el argumento es literal o variable propagada a literal, se verifica existencia previa.
  - `makedir`, `run`, `log`: validaciones básicas (por ejemplo, `run ""` se considera inválido si es literal/propagado)

- Mensajes de error:
  - Se lanza `SemanticError` con mensajes que comienzan con `[Error Semántico]` y, cuando está disponible, incluyen `Línea X, Columna Y:`.
  - Ejemplos:
    - `[Error Semántico] Línea 1, Columna 5: Variable 'NO_EXISTE' usada en interpolación antes de ser declarada.`
    - `[Error Semántico] Línea 2, Columna 1: Origen no encontrado: 'archivo.txt'.`

Cómo extender el analizador

- Añadir nuevos nodos: si añades nuevas clases en `core/ast_nodes.py`, asegúrate de que el `core/parser.py` cree esos nodos y (si procede) llame a `set_pos(token)` para que el analizador semántico pueda reportar ubicación.
- Reglas adicionales: en `core/semantic.py` sigue el patrón de `SemanticAnalyzer._visit_statement` y crea métodos `_check_<comando>` para centralizar validaciones. Usa `_resolve_const_or_literal(expr, consts)` para intentar obtener un valor estático sin ejecutar código.
- Posición en errores: los nodos tienen `line` y `column` (rellenados por el parser). Usa `self._format_pos(node)` para anteponer posición en los mensajes.

Detalles de implementación y ejemplos
----------------------------------

1) `set_pos` en nodos AST

- Propósito: asignar `line` y `column` a un nodo para que el analizador semántico pueda informar la posición exacta cuando detecte un error.
- Ejemplo (AST):

```python
class IfStatementNode(StatementNode):
  def __init__(self, condition, if_body, else_body=None):
    self.condition = condition
    self.if_body = if_body
    self.else_body = else_body
    self.line = None
    self.column = None

  def set_pos(self, token):
    if token is None:
      return
    self.line = getattr(token, 'line', None)
    self.column = getattr(token, 'column', None)
```

- El `parser` debe establecer la posición al crear el nodo:

```python
if_tok = self._expect('IF')
node = IfStatementNode(condition, if_body, else_body)
node.set_pos(if_tok)
```

2) `tmp_path` en tests

- Para tests que crean archivos o directorios, usa la fixture `tmp_path` de pytest para no crear artefactos en el repositorio y evitar colisión con archivos verdaderos.
- Ejemplo:

```python
def test_copy_destination_parent_missing_raises(tmp_path: Path):
  src_file = tmp_path / 'src_tmp.txt'
  src_file.write_text('hola')
  dest = 'nonexistent_parent_dir/sub/dest.txt'
  src = f'copy "{src_file}" to "{dest}"\n'
  with pytest.raises(SemanticError):
    parse_and_check(src)
```

3) Ejemplo de error semántico con `line` y `column`

- Script de ejemplo que produce un `SemanticError` por interpolación con variable no definida:

```sl
log "Hola ${NO_EXISTE}"
```

- Mensaje esperado (ejemplo):

```
[Error Semántico] Línea 1, Columna 5: Variable 'NO_EXISTE' usada en interpolación antes de ser declarada.
```

- En el caso de IF, si el error proviene de la condición o del cuerpo y el nodo tiene `set_pos` asignado por el parser, el `format_pos` incluirá la posición del `IF` en el mensaje de error.


Pruebas y CI

-- Tests unitarios: los tests semánticos están en `pruebas/test_semantic.py`. Ejecutar localmente con:

```powershell
$env:PYTHONPATH=(Get-Location).Path; pytest -q
```

Nota: `run_semantic_test.py` es un script de ejemplo que muestra cómo se realiza el flujo: tokenización → parseo → chequeo semántico → ejecución (si no hay errores). Puedes ejecutarlo manualmente con:

```powershell
$env:PYTHONPATH=(Get-Location).Path; python run_semantic_test.py
```
Este script está diseñado para demostración; `pytest` es la forma recomendada de ejecutar tests automatizados.

- Dependencias: `requirements.txt` contiene `pytest`.
- CI: `.github/workflows/ci.yml` ejecuta `pytest` en Ubuntu y establece `PYTHONPATH` al root del repo para que los tests importen `core`.

Buenas prácticas

- No evalúes variables en tiempo de análisis salvo que sean literales o claramente propagadas desde asignaciones literales; evaluar expresiones arbitrarias en el analizador rompería la promesa "sin ejecutar nada".
- Mantén las comprobaciones idempotentes y sin efectos secundarios (usar solo `filesystem.exists` para lecturas es aceptable).

Checklist para añadir una nueva regla semántica

1. Añadir el nodo en `core/ast_nodes.py` (incluir `set_pos`).
2. Modificar `core/parser.py` para crear el nodo e invocar `set_pos(tok)`.
3. Implementar la validación en `core/semantic.py` añadiendo un método `_check_<algo>(...)` y llamándolo desde `_visit_statement`.
4. Escribir tests en `pruebas/` que cubran casos positivos y negativos.
5. Ejecutar `pytest` y revisar mensajes.

Contacto y mantenimiento

- Este documento puede ampliarse con ejemplos concretos de scripts y errores comunes. Para cambios mayores (p. ej. análisis de flujo avanzado) añade diseño en `documentacion/arquitectura.md` antes de implementar.

Ejemplos de uso

A continuación se muestran scripts de ejemplo (`.sl`) y el comportamiento semántico esperado. También se han creado archivos reales bajo `documentacion/ejemplos_semantica/` con estos contenidos.

1) Interpolación con variable definida (OK)

Archivo: `documentacion/ejemplos_semantica/ejemplo_ok.sl`

```sl
set nombre = "Ema"
log "Hola ${nombre}"
```

Resultado esperado: no debe generar `SemanticError` y la ejecución es segura.

2) Interpolación con variable NO definida (ERROR semántico)

Archivo: `documentacion/ejemplos_semantica/ejemplo_missing_var.sl`

```sl
log "Hola ${NO_EXISTE}"
```

Resultado esperado: `SemanticError` indicando que la variable usada en interpolación no fue declarada. Ejemplo:

```
[Error Semántico] Línea 1, Columna 6: Variable 'NO_EXISTE' usada en interpolación antes de ser declarada.
```

3) `copy` con origen literal inexistente (ERROR semántico)

Archivo: `documentacion/ejemplos_semantica/ejemplo_copy_missing.sl`

```sl
copy "archivo_inexistente.txt" to "copia.txt"
```

Resultado esperado: `SemanticError` indicando que el origen no existe.

4) `copy` con variable propagada (OK si el archivo existe)

Archivo: `documentacion/ejemplos_semantica/ejemplo_prop_var.sl`

```sl
set src = "archivo_real.txt"
copy src to "copia.txt"
```

Resultado esperado: si `archivo_real.txt` existe (según `biblioteca/filesystem` y el `ROOT`), el analizador no reporta error; si no existe, se producirá `SemanticError`.

5) `run` vacío (ERROR semántico)

Archivo: `documentacion/ejemplos_semantica/ejemplo_run_empty.sl`

```sl
run ""
```

Resultado esperado: `SemanticError` indicando comando vacío.

*** Fin del documento de análisis semántico ***
