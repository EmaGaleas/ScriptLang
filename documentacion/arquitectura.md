
`La arquitectura modular de ScriptLang facilita su mantenimiento y escalabilidad.`
`Cada componente cumple una función específica dentro del flujo de análisis y ejecución, permitiendo extender el lenguaje con nuevos comandos o estructuras de control en el futuro.`

## Flujo de ejecución

```
main.py
   ↓
Lexer → tokens
   ↓
Parser → AST
   ↓
SemanticAnalyzer → validación
   ↓
Interpreter → ejecución
   ↓
Logger → registro de resultados
```

## Descripción de las características


 **main.py**
    `Punto de entrada. Coordina el proceso completo de análisis y ejecución.`

 **Lexer**
   `Convierte el código fuente en una secuencia de tokens según la gramática BNF.`

 **Parser**
   `Construye el Árbol de Sintaxis Abstracta (AST) siguiendo las reglas de la BNF.`

 **Semantic Analyzer**
   `Valida nombres de variables, tipos y contexto (por ejemplo, existencia de archivos o asignaciones previas).`

 **Interpreter**
   `Ejecuta las instrucciones del AST directamente, interactuando con el sistema operativo.`

 **Logger**
   `Registra las acciones realizadas y los errores ocurridos durante la ejecución.`