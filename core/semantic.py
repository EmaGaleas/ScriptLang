from typing import List, Set

from core.ast_nodes import (
    ProgramNode, AssignmentNode, VariableRefNode, StringLiteralNode,
    CopyCommandNode, MoveCommandNode, DeleteCommandNode, MakeDirCommandNode,
    RunCommandNode, LogCommandNode, IfStatementNode,
)


class SemanticError(Exception):
    pass


class SemanticAnalyzer:

    def __init__(self):
        self.errors: List[str] = []

    def analyze(self, program: ProgramNode) -> List[str]:
        self.errors = []
        defined: Set[str] = set()
        self._visit_statements(program.statements, defined)
        return self.errors

    # === Visitors ===
    def _visit_statements(self, stmts: List, defined: Set[str]):
        for stmt in stmts:
            self._visit_statement(stmt, defined)

    def _visit_statement(self, stmt, defined: Set[str]):
        if isinstance(stmt, AssignmentNode):
            self._check_expression(stmt.value, defined)
            defined.add(stmt.variable_name)
            return

        if isinstance(stmt, (CopyCommandNode, MoveCommandNode)):
            self._check_expression(stmt.source, defined)
            self._check_expression(stmt.destination, defined)
            return

        if isinstance(stmt, DeleteCommandNode):
            self._check_expression(stmt.target, defined)
            return

        if isinstance(stmt, MakeDirCommandNode):
            self._check_expression(stmt.path, defined)
            return

        if isinstance(stmt, RunCommandNode):
            self._check_expression(stmt.program, defined)
            return

        if isinstance(stmt, LogCommandNode):
            self._check_expression(stmt.message, defined)
            return

        if isinstance(stmt, IfStatementNode):
            self._check_expression(stmt.condition.path, defined)#comprobar la condición si cumple con el estado actual

            defined_if = set(defined)
            self._visit_statements(stmt.if_body, defined_if)

            if stmt.else_body is not None:
                defined_else = set(defined)
                self._visit_statements(stmt.else_body, defined_else)

            return

    def _check_expression(self, expr, defined: Set[str]):
        if expr is None:
            return

        if isinstance(expr, VariableRefNode):
            name = expr.name
            if name not in defined:
                self.errors.append(f"[Error Semántico] Variable '{name}' usada antes de ser declarada.")
            return

        if isinstance(expr, StringLiteralNode):
            return



def check_semantics(program_node: ProgramNode):
    analyzer = SemanticAnalyzer()
    errors = analyzer.analyze(program_node)
    if errors:
        raise SemanticError("\n".join(errors))


__all__ = ["SemanticAnalyzer", "SemanticError", "check_semantics"]
