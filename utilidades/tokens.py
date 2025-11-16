"""
Definición de los tokens reconocidos por el lenguaje ScriptLang.
Este módulo lista las palabras clave, símbolos y tipos de token
que el analizador léxico (Lexer) identificará en los scripts .sl
"""

# Palabras clave del lenguaje
KEYWORDS = {
    "set": "SET",
    "copy": "COPY",
    "move": "MOVE",
    "delete": "DELETE",
    "makedir": "MAKEDIR",
    "run": "RUN",
    "log": "LOG",
    "if": "IF",
    "else": "ELSE",
    "exists": "EXISTS",
    "to": "TO"
}

# Símbolos y operadores
SYMBOLS = {
    "=": "EQUAL",
    "{": "LBRACE",
    "}": "RBRACE",
    "$": "DOLLAR"
}

# Tipos de token generales 
TOKEN_TYPES = {
    "VAR": "VAR",    # Nombres de variables (IDENT) (Se puede cambiar)
    "STRING": "STRING",  # Cadenas entre comillas ("texto") 
    "END": "END"         # Fin de archivo (Tambien se puede cambiar)
}
