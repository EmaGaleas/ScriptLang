from utilidades.tokens import KEYWORDS, SYMBOLS, TOKEN_TYPES
from utilidades.errores import AuxError
class Token:
    __slots__ = ("type", "value", "line", "column")

    def __init__(self, type_, value, line, column):
        self.type, self.value, self.line, self.column = type_, value, line, column

    def __repr__(self):
        return f"Token({self.type}, {self.value}, line={self.line}, col={self.column})"

class Lexer:
    def __init__(self, src: str):
        self.src, self.pos, self.line, self.col = src, 0, 1, 1
        self.len = len(src)

    # PUBLICO
    def tokenize(self):
        tokens = []
        add = tokens.append  # microoptimizacion

        while not self._eof():
            c = self._peek()

            if c.isspace():
                self._consume(str.isspace)
            elif c == '#':
                self._consume(lambda ch: ch != '\n')
                self._advance()  # salto de línea
            elif c == '"':
                add(self._string())
            elif c.isalpha() or c == '_':
                add(self._identifier())
            elif c in SYMBOLS:
                add(self._symbol())
            else:
                raise SyntaxError(f"Carácter inesperado '{c}' en línea {self.line}, columna {self.col}")

        add(Token(TOKEN_TYPES["END"], None, self.line, self.col))
        return tokens

    # TOKENS
    def _string(self):
        start_line, start_col = self.line, self.col
        self._advance()  # abre comillas
        val = []

        while not self._eof():
            c = self._peek()
            if c == '"':
                break
            if c == '\\' and self._peek(1) == '"':
                val.append('"')
                self._advance(2)
            else:
                val.append(self._advance())  # todo tal cual, no tocar $

        if self._eof():
            AuxError.illegal_char(c, self.line, self.col)

        self._advance()  # cierra comillas
        return Token(TOKEN_TYPES["STRING"], ''.join(val), start_line, start_col)


    def _identifier(self):
        start_line, start_col = self.line, self.col
        value = self._consume(lambda c: c.isalnum() or c == '_')
        return Token(KEYWORDS.get(value, TOKEN_TYPES["VAR"]), value, start_line, start_col)

    def _symbol(self):
        start_line, start_col = self.line, self.col
        c = self._advance()
        return Token(SYMBOLS[c], c, start_line, start_col)

    # UTILIDADES
    def _consume(self, cond):
        start = self.pos
        while not self._eof() and cond(self._peek()):
            self._advance()
        return self.src[start:self.pos]

    def _advance(self, n=1):
        chunk = self.src[self.pos:self.pos + n]
        for ch in chunk:
            self.line += ch == '\n'
            self.col = 1 if ch == '\n' else self.col + 1
        self.pos += n
        return chunk

    def _peek(self, offset=0):
        return self.src[self.pos + offset] if self.pos + offset < self.len else '\0'

    def _eof(self):
        return self.pos >= self.len
