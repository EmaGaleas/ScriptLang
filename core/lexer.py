from utilidades.tokens import KEYWORDS, SYMBOLS, TOKEN_TYPES

class Token:
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
        self.position = 0
        self.line = 1
        self.column = 1

    def tokenize(self):
        tokens = []

        while not self._is_at_end():
            current_char = self._peek()

            if current_char.isspace():
                self._consume_whitespace()
            elif current_char == '#':
                self._consume_comment()
            elif current_char == '"':
                tokens.append(self._consume_string())
            elif current_char.isalpha() or current_char == '_':
                tokens.append(self._consume_identifier_or_keyword())
            elif current_char in SYMBOLS:
                tokens.append(self._consume_symbol())
            else:
                raise Exception(f"Unexpected character '{current_char}' at line {self.line}, column {self.column}")

        tokens.append(Token(TOKEN_TYPES["END"], None, self.line, self.column))
        return tokens

    def _consume_whitespace(self):
        while not self._is_at_end() and self._peek().isspace():
            self._advance()

    def _consume_comment(self):
        while not self._is_at_end() and self._peek() != '\n':
            self._advance()
        self._advance()  # Consume newline

    def _consume_string(self):
        start_line, start_col = self.line, self.column
        self._advance()  # Skip opening quote
        value = ""

        while not self._is_at_end() and self._peek() != '"':
            if self._peek() == '\\' and self._peek(1) == '"':
                value += '"'
                self._advance(2)
            elif self._peek() == '$':  # Variable reference inside string
                self._advance()
                var_name = self._consume_while(lambda c: c.isalnum() or c == '_')
                value += f"${{{var_name}}}"  # Template interpolation
            else:
                value += self._advance()

        if self._is_at_end():
            raise Exception(f"Unterminated string at line {start_line}, column {start_col}")

        self._advance()  # Skip closing quote
        return Token(TOKEN_TYPES["STRING"], value, start_line, start_col)

    def _consume_identifier_or_keyword(self):
        start_line, start_col = self.line, self.column
        value = self._consume_while(lambda c: c.isalnum() or c == '_')

        if value in KEYWORDS:
            return Token(KEYWORDS[value], value, start_line, start_col)
        else:
            return Token(TOKEN_TYPES["VAR"], value, start_line, start_col)

    def _consume_symbol(self):
        start_line, start_col = self.line, self.column
        char = self._advance()
        return Token(SYMBOLS[char], char, start_line, start_col)

    def _consume_while(self, condition):
        result = ""
        while not self._is_at_end() and condition(self._peek()):
            result += self._advance()
        return result

    def _advance(self, step=1):
        char = self.source[self.position:self.position + step]
        for _ in range(step):
            if self._peek() == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1

            self.position += 1

        return char

    def _peek(self, offset=0):
        if self.position + offset < self.length:
            return self.source[self.position + offset]
        return '\0'

    def _is_at_end(self):
        return self.position >= self.length
