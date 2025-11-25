from typing import List, Set, Dict, Optional
import re
from pathlib import Path

from biblioteca import filesystem

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
        # consts: mapping variable name -> literal string value when known (propagación simple)
        consts: Dict[str, str] = {}
        self._visit_statements(program.statements, defined, consts)
        return self.errors

    # === Visitors ===
    def _visit_statements(self, stmts: List, defined: Set[str], consts: Dict[str, str]):
        for stmt in stmts:
            self._visit_statement(stmt, defined, consts)

    def _visit_statement(self, stmt, defined: Set[str], consts: Dict[str, str]):
        if isinstance(stmt, AssignmentNode):
            self._check_expression(stmt.value, defined, consts)
            # Si la asignación es una literal string, la consideramos constante
            if isinstance(stmt.value, StringLiteralNode):
                consts[stmt.variable_name] = stmt.value.value
            else:
                # invalidar posible constante previa
                if stmt.variable_name in consts:
                    del consts[stmt.variable_name]
            defined.add(stmt.variable_name)
            return

        if isinstance(stmt, (CopyCommandNode, MoveCommandNode)):
            # Comprobaciones centralizadas
            self._check_copy_move(stmt, defined, consts)
            return

        if isinstance(stmt, DeleteCommandNode):
            self._check_delete(stmt, defined, consts)
            return

        if isinstance(stmt, MakeDirCommandNode):
            self._check_expression(stmt.path, defined, consts)
            return

        if isinstance(stmt, RunCommandNode):
            self._check_expression(stmt.program, defined, consts)
            # Si el argumento de RUN es literal o variable conocida, evitar comandos vacíos
            prog_val = self._resolve_const_or_literal(stmt.program, consts)
            if prog_val is not None:
                if not str(prog_val).strip():
                    self.errors.append(self._format_pos(stmt) + "Comando RUN vacío no permitido.")
            return

        if isinstance(stmt, LogCommandNode):
            self._check_expression(stmt.message, defined, consts)
            return

        if isinstance(stmt, IfStatementNode):
            self._check_expression(stmt.condition.path, defined, consts)  # comprobar la condición

            defined_if = set(defined)
            consts_if = dict(consts)
            self._visit_statements(stmt.if_body, defined_if, consts_if)

            if stmt.else_body is not None:
                defined_else = set(defined)
                consts_else = dict(consts)
                self._visit_statements(stmt.else_body, defined_else, consts_else)

            return

    def _check_expression(self, expr, defined: Set[str], consts: Dict[str, str]):
        if expr is None:
            return

        if isinstance(expr, VariableRefNode):
            name = expr.name
            if name not in defined:
                self.errors.append(self._format_pos(expr) + f"Variable '{name}' usada antes de ser declarada.")
            return

        if isinstance(expr, StringLiteralNode):
            # Buscar variables interpoladas del tipo ${VAR} y comprobar que estén definidas
            pattern = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}")
            for m in pattern.finditer(expr.value):
                name = m.group(1)
                if name not in defined:
                    self.errors.append(self._format_pos(expr) + f"Variable '{name}' usada en interpolación antes de ser declarada.")
            return

    # --- helpers and command-specific checks ---
    def _format_pos(self, node) -> str:
        if node is None:
            return "[Error Semántico] "
        line = getattr(node, 'line', None)
        col = getattr(node, 'column', None)
        if line is not None and col is not None:
            return f"[Error Semántico] Línea {line}, Columna {col}: "
        return "[Error Semántico] "

    def _resolve_const_or_literal(self, expr, consts: Dict[str, str]) -> Optional[str]:
        # Devuelve el valor literal si se puede conocer estáticamente
        if isinstance(expr, StringLiteralNode):
            return expr.value
        if isinstance(expr, VariableRefNode):
            return consts.get(expr.name)
        return None

    def _check_copy_move(self, node, defined: Set[str], consts: Dict[str, str]):
        # comprobar expresiones básicas
        self._check_expression(node.source, defined, consts)
        self._check_expression(node.destination, defined, consts)

        # revisar existencia del origen si es literal o variable conocida
        src_val = self._resolve_const_or_literal(node.source, consts)
        if src_val is not None:
            try:
                if not filesystem.exists(src_val):
                    self.errors.append(self._format_pos(node) + f"Origen no encontrado: '{src_val}'.")
            except Exception as e:
                self.errors.append(self._format_pos(node) + f"Error comprobando existencia de '{src_val}': {e}")

        # revisar destino parent si destino es literal
        dst_val = self._resolve_const_or_literal(node.destination, consts)
        if dst_val is not None:
            try:
                # si el destino tiene padre, comprobar que exista
                p = Path(dst_val)
                parent = str(p.parent) if p.parent else None
                if parent:
                    if not filesystem.exists(parent):
                        self.errors.append(self._format_pos(node) + f"Directorio destino no existente: '{parent}'.")
            except Exception as e:
                self.errors.append(self._format_pos(node) + f"Error comprobando destino '{dst_val}': {e}")

    def _check_delete(self, node, defined: Set[str], consts: Dict[str, str]):
        self._check_expression(node.target, defined, consts)
        tgt_val = self._resolve_const_or_literal(node.target, consts)
        if tgt_val is not None:
            try:
                if not filesystem.exists(tgt_val):
                    self.errors.append(self._format_pos(node) + f"Target para DELETE no encontrado: '{tgt_val}'.")
            except Exception as e:
                self.errors.append(self._format_pos(node) + f"Error comprobando DELETE '{tgt_val}': {e}")



def check_semantics(program_node: ProgramNode):
    analyzer = SemanticAnalyzer()
    errors = analyzer.analyze(program_node)
    if errors:
        raise SemanticError("\n".join(errors))

def check(program_node: ProgramNode):
    """Compatibilidad: nombre público `check()` solicitado.

    Lanza `SemanticError` si hay errores semánticos.
    """
    return check_semantics(program_node)


__all__ = ["SemanticAnalyzer", "SemanticError", "check_semantics", "check"]
