
from utilidades.tokens import TOKEN_TYPES
from utilidades.errores import AuxError
from core.ast_nodes import (
    ProgramNode, AssignmentNode, CopyCommandNode, MoveCommandNode,
    DeleteCommandNode, MakeDirCommandNode, RunCommandNode, LogCommandNode,
    IfStatementNode, ExistsConditionNode, StringLiteralNode, VariableRefNode,
)

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    # UTILIDADES
    def _peek(self, offset=0):
        return self.tokens[self.pos + offset] if self.pos + offset < len(self.tokens) else None

    def _current(self):
        return self._peek(0)

    def _advance(self):
        tok = self._current()
        if tok:
            self.pos += 1
        return tok

    def _expect(self, ttype):
        tok = self._current()
        if tok is None or tok.type != ttype:
            AuxError.expected(tok, [ttype])
        return self._advance()

    def _accept(self, ttype):
        tok = self._current()
        if tok and tok.type == ttype:
            return self._advance()
        return None

    # PARSER GENERAL
    def parse(self):
        stmts = []
        while True:
            cur = self._current()
            if cur is None or cur.type == TOKEN_TYPES["END"]:
                break
            stmts.append(self._parse_statement())
        return ProgramNode(stmts)

    # STATEMENTS
    def _parse_statement(self):
        cur = self._current()
        if cur is None:
            AuxError.unexpected_eof(["declaración válida"])

        if cur.type == TOKEN_TYPES["VAR"]:
            next_tok = self._peek(1)
            if next_tok and next_tok.type == "EQUAL":
                return self._parse_assignment()
            AuxError.expected(cur, ["="])

        if cur.type == "SET":
            return self._parse_assignment_set()

        if cur.type in ("COPY", "MOVE", "DELETE", "MAKEDIR", "RUN", "LOG"):
            return self._parse_command()

        if cur.type == "IF":
            return self._parse_if()

        AuxError.unexpected(cur)

    # ASIGNACIONES
    def _parse_assignment_set(self):
        self._expect("SET")
        var_tok = self._expect(TOKEN_TYPES["VAR"])
        self._expect("EQUAL")
        return AssignmentNode(var_tok.value, self._parse_expression())

    def _parse_assignment(self):
        var_tok = self._expect(TOKEN_TYPES["VAR"])
        self._expect("EQUAL")
        return AssignmentNode(var_tok.value, self._parse_expression())

    # COMANDOS
    def _parse_command(self):
        cur = self._advance()

        if cur.type in ("COPY", "MOVE"):
            src = self._parse_expression()
            self._expect("TO")
            dst = self._parse_expression()
            return CopyCommandNode(src, dst) if cur.type == "COPY" else MoveCommandNode(src, dst)

        if cur.type == "DELETE":
            return DeleteCommandNode(self._parse_expression())

        if cur.type == "MAKEDIR":
            return MakeDirCommandNode(self._parse_expression())

        if cur.type == "RUN":
            return RunCommandNode(self._parse_expression())

        if cur.type == "LOG":
            return LogCommandNode(self._parse_expression())

        AuxError.unexpected(cur)

    # IF / BLOQUES
    def _parse_if(self):
        self._expect("IF")
        cond = self._current()
        if cond is None or cond.type != "EXISTS":
            AuxError.expected(cond, ["EXISTS"])
        self._advance()

        expr = self._parse_expression()
        condition = ExistsConditionNode(expr)

        self._expect("LBRACE")
        if_body = self._parse_block()

        else_body = None
        if self._accept("ELSE"):
            self._expect("LBRACE")
            else_body = self._parse_block()

        return IfStatementNode(condition, if_body, else_body)

    def _parse_block(self):
        stmts = []
        while True:
            cur = self._current()
            if cur is None:
                AuxError.unexpected_eof(["}"])
            if cur.type == "RBRACE":
                self._advance()
                break
            stmts.append(self._parse_statement())
        return stmts

    # EXPRESIONES
    def _parse_expression(self):
        cur = self._current()
        if cur is None:
            AuxError.unexpected_eof(["expresión"])

        if cur.type == TOKEN_TYPES["STRING"]:
            return StringLiteralNode(self._advance().value)

        if cur.type == TOKEN_TYPES["VAR"]:
            return VariableRefNode(self._advance().value)

        AuxError.expected(cur, ["STRING", "VAR"])

def parse_tokens(tokens):
    return Parser(tokens).parse()
