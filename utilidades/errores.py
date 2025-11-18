# errores.py

class AuxError:

    # ERRORES DE SINTAXIS
    @staticmethod
    def expected(token, esperado):
        """Error cuando se esperaba uno o varios tokens específicos."""
        if token is None:
            return AuxError.unexpected_eof(esperado)

        linea = token.line
        col = token.column
        encontrado = token.value
        esperado_fmt = ", ".join(esperado)

        raise SyntaxError(
            f"[Error Sintáctico] Línea {linea}, Columna {col}: "
            f"Se encontró '{encontrado}'. Se esperaba: {esperado_fmt}."
        )

    @staticmethod
    def unexpected(token):
        """Error para token inesperado en parser."""
        if token is None:
            return AuxError.unexpected_eof(["token válido"])

        linea = token.line
        col = token.column

        raise SyntaxError(
            f"[Error Sintáctico] Línea {linea}, Columna {col}: "
            f"Token inesperado '{token.value}'."
        )

    @staticmethod
    def unexpected_eof(esperado):
        """Fin inesperado de archivo."""
        esperado_fmt = ", ".join(esperado)
        raise SyntaxError(
            f"[Error Sintáctico] Fin de archivo inesperado. "
            f"Se esperaba: {esperado_fmt}."
        )

    # ERRORES LÉXICOS
    @staticmethod
    def illegal_char(char, linea, col):
        """Caracter no reconocido por el lenguaje."""
        raise SyntaxError(
            f"[Error Léxico] Línea {linea}, Columna {col}: "
            f"Carácter ilegal '{char}'."
        )

    @staticmethod
    def unterminated_string(linea, col):
        """Cadena sin cerrar."""
        raise SyntaxError(
            f"[Error Léxico] Línea {linea}, Columna {col}: "
            f"Cadena string sin cerrar."
        )

    @staticmethod
    def invalid_escape(char, linea, col):
        """Escape inválido dentro de string."""
        raise SyntaxError(
            f"[Error Léxico] Línea {linea}, Columna {col}: "
            f"Secuencia de escape inválida '\\{char}'."
        )
