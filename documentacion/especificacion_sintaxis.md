---
## Objetivos del Lenguaje ScriptLang

Automatizar tareas básicas del SO mediante scripts `.sl` legibles y cortos.
---

## Alcance

### ¿Qué puede hacer?

- **Operaciones de archivos y directorios**

  - `copy`, `move`, `delete`, `mkdir`

- **Ejecución de comandos del sistema**

  - `run "<cmd>"`

- **Registro de acciones y errores**

  - `log "<mensaje>"`

- **Variables y sustitución dentro del string**

  - `set x = "valor"`, uso puede ser `"$x"`

- **Condicional simple basada en existencia de rutas**

  - `if exists "<ruta>" { ... } else { ... }`

- **Comentarios de línea**

  - `#` o `//`

---

### ¿Qué no puede hacer?

- Bucles (`for`, `while`), funciones, módulos o paquetes.
- Expresiones aritméticas o booleanas generales.
- Concurrencia, red (HTTP, sockets) o base de datos.
- IO interactiva, UI o scheduler.

---

## Sintaxis del Lenguaje

### Palabras Clave

`Set`, `Copy`, `Move`, `Delete`, `Mkdir`, `Run`, `Log`, `If`, `Else`, `Exists`, `To`

---

### Reglas del lenguaje

- String siempre con comillas dobles `"..."`.
- Se toma como comentario cualquier texto después de `#` hasta el fin de línea.
- Los bloques van con llaves `{ ... }`.
- Los comandos van en minúscula, uno por línea.
- Las variables (por ejemplo: `set nombre = "valor"`) se expanden como `"$nombre"` dentro de strings.

---

### Algunos patrones de comando

```sl
set <ident> = <string>
copy <string> to <string>
move <string> to <string>
delete <string>
mkdir <string>
run <string>
log <string>
if exists <string> { <statements> } [else { <statements> }]
```

---

## Gramática base (BNF)

```
<program>        ::= <stmt_list>
<stmt_list>      ::= <stmt> | <stmt_list> <stmt>
<stmt>           ::= <assign> | <command> | <if_stmt>
<assign>         ::= "set" IDENT "=" STRING
<command>        ::= <copy> | <move> | <delete> | <mkdir> | <run> | <log>
<copy>           ::= "copy" STRING "to" STRING
<move>           ::= "move" STRING "to" STRING
<delete>         ::= "delete" STRING
<mkdir>          ::= "mkdir" STRING
<run>            ::= "run" STRING
<log>            ::= "log" STRING
<if_stmt>        ::= "if" "exists" STRING "{" <stmt_list> "}" <else_opt>
<else_opt>       ::= ε | "else" "{" <stmt_list> "}"
IDENT            ::= [A-Za-z_][A-Za-z0-9_]*
STRING           ::= '"' { (carácter no comillas) | ('\"') | <varref> } '"'
<varref>         ::= "$" IDENT
```
