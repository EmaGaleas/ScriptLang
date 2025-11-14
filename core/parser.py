# parser.py
from utilidades.tokens import TOKEN_TYPES
from core.ast_nodes import (
    ProgramNode, AssignmentNode, CopyCommandNode, MoveCommandNode,
    DeleteCommandNode, MakeDirCommandNode, RunCommandNode, LogCommandNode,
    IfStatementNode, ExistsConditionNode, StringLiteralNode, VariableRefNode,
    CommandNode, StatementNode
)

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    # --- Utilities ---
    def _peek(self, offset=0):
        if self.pos + offset < len(self.tokens):
            return self.tokens[self.pos + offset]
        return None

    def _current(self):
        return self._peek(0)

    def _advance(self):
        tok = self._current()
        if tok is not None:
            self.pos += 1
        return tok

    def _expect(self, ttype, msg=None):
        tok = self._current()
        if tok is None or tok.type != ttype:
            if msg is None:
                msg = f"Se esperaba token {ttype} pero se obtuvo {tok}"
            raise SyntaxError(msg)
        return self._advance()

    def _accept(self, ttype):
        tok = self._current()
        if tok is not None and tok.type == ttype:
            return self._advance()
        return None

    def parse(self):
        stmts = []
        while True:
            cur = self._current()
            if cur is None or cur.type == TOKEN_TYPES["END"]:
                break
            # Skip stray ENDs if any
            if cur.type == TOKEN_TYPES.get("END"):
                break
            stmts.append(self._parse_statement())
        return ProgramNode(stmts)

    # --- Statements ---
    def _parse_statement(self):
        cur = self._current()
        if cur is None:
            raise SyntaxError("Fin inesperado de entrada al parsear declaración")

        # Assignment: VAR = expr
        if cur.type == TOKEN_TYPES["VAR"]:
            # lookahead to see if assignment or command starting with var (we use var only for set)
            # For a "set" style they might prefer `set x = "..."` but lexer maps "set" to SET.
            # Here we support both "set x = ..." and direct assignment "x = ..."
            next_tok = self._peek(1)
            if next_tok and next_tok.type == "EQUAL":
                return self._parse_assignment()
            # else fallthrough: treat as error
            raise SyntaxError(f"Identificador '{cur.value}' no esperado sin '=' en línea {cur.line}")

        # Keywords
        if cur.type == "SET":
            return self._parse_assignment_set()

        if cur.type in ("COPY", "MOVE", "DELETE", "MAKEDIR", "RUN", "LOG"):
            return self._parse_command()

        if cur.type == "IF":
            return self._parse_if()

        raise SyntaxError(f"Declaración desconocida: {cur} (línea {cur.line})")

    def _parse_assignment_set(self):
        # set x = expr
        set_tok = self._expect("SET")
        var_tok = self._expect(TOKEN_TYPES["VAR"], f"Se esperaba nombre de variable después de 'set' (línea {set_tok.line})")
        self._expect("EQUAL", f"Se esperaba '=' después de nombre de variable (línea {var_tok.line})")
        expr = self._parse_expression()
        return AssignmentNode(var_tok.value, expr)

    def _parse_assignment(self):
        # x = expr
        var_tok = self._expect(TOKEN_TYPES["VAR"])
        self._expect("EQUAL", f"Se esperaba '=' después de nombre de variable (línea {var_tok.line})")
        expr = self._parse_expression()
        return AssignmentNode(var_tok.value, expr)

    # --- Commands ---
    def _parse_command(self):
        cur = self._current()
        if cur.type == "COPY":
            self._advance()
            src = self._parse_expression()
            # expect 'TO'
            self._expect("TO", f"Se esperaba 'to' después de ruta origen en copy (línea {cur.line})")
            dst = self._parse_expression()
            return CopyCommandNode(src, dst)

        if cur.type == "MOVE":
            self._advance()
            src = self._parse_expression()
            self._expect("TO", f"Se esperaba 'to' después de ruta origen en move (línea {cur.line})")
            dst = self._parse_expression()
            return MoveCommandNode(src, dst)

        if cur.type == "DELETE":
            self._advance()
            target = self._parse_expression()
            return DeleteCommandNode(target)

        if cur.type == "MAKEDIR":
            self._advance()
            path = self._parse_expression()
            return MakeDirCommandNode(path)

        if cur.type == "RUN":
            self._advance()
            prog = self._parse_expression()
            return RunCommandNode(prog)

        if cur.type == "LOG":
            self._advance()
            msg = self._parse_expression()
            return LogCommandNode(msg)

        raise SyntaxError(f"Comando no soportado: {cur}")

    # --- If / control structures ---
    def _parse_if(self):
        if_tok = self._expect("IF")
        # supported condition form: exists <expr>
        cond_tok = self._current()
        if cond_tok is None or cond_tok.type != "EXISTS":
            raise SyntaxError(f"Se esperaba 'exists' después de 'if' (línea {if_tok.line})")
        self._advance()
        path_expr = self._parse_expression()
        condition = ExistsConditionNode(path_expr)

        # parse if-body: expect LBRACE { statements }
        self._expect("LBRACE", f"Se esperaba '{{' para abrir el bloque 'if' (línea {if_tok.line})")
        if_body = self._parse_block()
        else_body = None
        # optional else
        if self._accept("ELSE"):
            self._expect("LBRACE", "Se esperaba '{' para abrir el bloque 'else'")
            else_body = self._parse_block()

        return IfStatementNode(condition, if_body, else_body)

    def _parse_block(self):
        stmts = []
        # parse until RBRACE
        while True:
            cur = self._current()
            if cur is None:
                raise SyntaxError("Bloque no cerrado, fin inesperado de entrada")
            if cur.type == "RBRACE":
                self._advance()  # consume '}'
                break
            stmts.append(self._parse_statement())
        return stmts

    # --- Expressions ---
    def _parse_expression(self):
        cur = self._current()
        if cur is None:
            raise SyntaxError("Se esperaba expresión pero se encontró fin de entrada")
        if cur.type == TOKEN_TYPES["STRING"]:
            tok = self._advance()
            # The lexer already produced interpolated forms like ${var} inside the string value.
            # For now we keep the whole string as a StringLiteralNode.
            return StringLiteralNode(tok.value)
        if cur.type == TOKEN_TYPES["VAR"]:
            tok = self._advance()
            return VariableRefNode(tok.value)
        raise SyntaxError(f"Expresión no válida: {cur} (línea {cur.line})")


# --- Helper function para uso externo ---
def parse_tokens(tokens):
    p = Parser(tokens)
    return p.parse()


# If you want to allow running this parser standalone for quick tests:
if __name__ == "__main__":
    from utilidades.lexer import Lexer
    src = '''
    set path = "/home/user"
    copy "/home/user/file.txt" to "/tmp/copied.txt"
    if exists "/tmp/copied.txt" {
        log "archivo existe"
    } else {
        log "no existe"
    }
    '''
    lex = Lexer(src)
    tokens = lex.tokenize()
    ast = parse_tokens(tokens)
    print(ast)
