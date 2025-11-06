from utilidades.tokens import KEYWORDS, SYMBOLS, TOKEN_TYPES

class Token:
    __slots__ = ("type", "value", "line", "column")  # Menor uso de memoria

    def __init__(self, type_, value, line, column):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type}, {self.value}, line={self.line}, col={self.column})"


class Lexer:
    def __init__(self, source_code):
        self.source = source_code
        self.length = len(source_code)
        self.pos = 0
        self.line = 1
        self.col = 1

    # === PÚBLICO ===
    def tokenize(self):
        tokens = []

        while not self._at_end():
            c = self._peek()

            if c.isspace():
                self._skip_whitespace()
            elif c == '#':
                self._skip_comment()
            elif c == '"':
                tokens.append(self._string())
            elif c.isalpha() or c == '_':
                tokens.append(self._identifier())
            elif c in SYMBOLS:
                tokens.append(self._symbol())
            else:
                raise SyntaxError(f"Carácter inesperado '{c}' en línea {self.line}, columna {self.col}")

        tokens.append(Token(TOKEN_TYPES["END"], None, self.line, self.col))
        return tokens

    # === PRIVADO ===
    def _skip_whitespace(self):
        self._consume_while(str.isspace)

    def _skip_comment(self):
        self._consume_while(lambda ch: ch != '\n')
        if not self._at_end():  # Consume newline
            self._advance()

    def _string(self):
        start_line, start_col = self.line, self.col
        self._advance()  # abre comillas
        value = []

        while not self._at_end():
            c = self._peek()
            if c == '"':
                break
            if c == '\\' and self._peek(1) == '"':
                value.append('"')
                self._advance(2)
            elif c == '$':
                self._advance()
                var_name = self._consume_while(lambda ch: ch.isalnum() or ch == '_')
                value.append(f"${{{var_name}}}")
            else:
                value.append(self._advance())

        if self._at_end():
            raise SyntaxError(f"Cadena sin cerrar en línea {start_line}, columna {start_col}")

        self._advance()  # cierra comillas
        return Token(TOKEN_TYPES["STRING"], ''.join(value), start_line, start_col)

    def _identifier(self):
        start_line, start_col = self.line, self.col
        value = self._consume_while(lambda c: c.isalnum() or c == '_')
        token_type = KEYWORDS.get(value, TOKEN_TYPES["VAR"])
        return Token(token_type, value, start_line, start_col)

    def _symbol(self):
        start_line, start_col = self.line, self.col
        c = self._advance()
        return Token(SYMBOLS[c], c, start_line, start_col)

    # === UTILIDADES ===
    def _consume_while(self, cond):
        result = []
        while not self._at_end() and cond(self._peek()):
            result.append(self._advance())
        return ''.join(result)

    def _advance(self, step=1):
        if self._at_end():
            return '\0'
        char = self.source[self.pos:self.pos + step]
        for c in char:
            if c == '\n':
                self.line += 1
                self.col = 1
            else:
                self.col += 1
        self.pos += step
        return char

    def _peek(self, offset=0):
        return self.source[self.pos + offset] if self.pos + offset < self.length else '\0'

    def _at_end(self):
        return self.pos >= self.length
