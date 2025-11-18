from __future__ import annotations

from typing import Dict, List
from core.ast_nodes import (
    ProgramNode, AssignmentNode, CopyCommandNode, StatementNode, MoveCommandNode, ExpressionNode,
    DeleteCommandNode, MakeDirCommandNode, RunCommandNode, LogCommandNode,
    IfStatementNode, ExistsConditionNode, StringLiteralNode, VariableRefNode,
)

class InterpreterError(Exception):
    pass

class Interpreter:
    def __init__(self) -> None:
        # Entorno simple: nombre -> valor (string)
        self.env: Dict[str, str] = {}

    # === Punto de entrada ===

    def run(self, program: ProgramNode) -> None:
        """Ejecuta un ProgramNode completo."""
        self._exec_statements(program.statements)

    # === Ejecución de statements ===

    def _exec_statements(self, statements: List[StatementNode]) -> None:
        for stmt in statements:
            self._exec_statement(stmt)

    def _exec_statement(self, stmt: StatementNode) -> None:
        # Asignaciones
        if isinstance(stmt, AssignmentNode):
            value = self._eval_expr(stmt.value)
            self.env[stmt.variable_name] = value
            return

        # Comandos de archivo / sistema / log
        if isinstance(stmt, CopyCommandNode):
            src = self._eval_expr(stmt.source)
            dst = self._eval_expr(stmt.destination)
            self._cmd_copy(src, dst)
            return

        if isinstance(stmt, MoveCommandNode):
            src = self._eval_expr(stmt.source)
            dst = self._eval_expr(stmt.destination)
            self._cmd_move(src, dst)
            return

        if isinstance(stmt, DeleteCommandNode):
            target = self._eval_expr(stmt.target)
            self._cmd_delete(target)
            return

        if isinstance(stmt, MakeDirCommandNode):
            path = self._eval_expr(stmt.path)
            self._cmd_makedir(path)
            return

        if isinstance(stmt, RunCommandNode):
            program = self._eval_expr(stmt.program)
            self._cmd_run(program)
            return

        if isinstance(stmt, LogCommandNode):
            msg = self._eval_expr(stmt.message)
            self._cmd_log(msg)
            return

        # If / else
        if isinstance(stmt, IfStatementNode):
            self._exec_if(stmt)
            return

        raise InterpreterError(f"Statement no soportado: {type(stmt).__name__}")

    # === Expresiones ===

    def _eval_expr(self, expr: ExpressionNode) -> str:
        if isinstance(expr, StringLiteralNode):
            # La cadena puede traer ${VAR} adentro → interpolamos.
            return self._interpolate(expr.value)

        if isinstance(expr, VariableRefNode):
            if expr.name not in self.env:
                raise InterpreterError(f"Variable '{expr.name}' usada sin valor en tiempo de ejecución.")
            return self.env[expr.name]

        raise InterpreterError(f"Expresión no soportada: {type(expr).__name__}")

    def _interpolate(self, text: str) -> str:
        """
        Reemplaza patrones del tipo ${VAR} con el valor de la variable en el entorno.
        Si la variable no existe, se reemplaza por cadena vacía.
        """
        import re

        pattern = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}")

        def repl(match: re.Match) -> str:
            name = match.group(1)
            return self.env.get(name, "")

        return pattern.sub(repl, text)

    # === If / Exists ===

    def _exec_if(self, node: IfStatementNode) -> None:
        cond = node.condition
        if not isinstance(cond, ExistsConditionNode):
            raise InterpreterError("Solo se soporta condición EXISTS en IF.")

        path = self._eval_expr(cond.path)
        if self._check_exists(path):
            self._exec_statements(node.if_body)
        elif node.else_body is not None:
            self._exec_statements(node.else_body)

    def _check_exists(self, path: str) -> bool:
        """
        Verifica la condición EXISTS(path).
        Aquí SOLO definimos la estructura. Más adelante esto se puede delegar
        a biblioteca.filesystem.exists(path) o similar.
        """
        # TODO: integrar con biblioteca.filesystem
        print(f"[CHECK EXISTS] {path}")
        return False  # Por ahora, siempre 'no existe'

    # === Handlers de comandos (estructura base) ===

    def _cmd_copy(self, src: str, dst: str) -> None:
        # TODO: conectar con biblioteca.filesystem.copy(src, dst)
        print(f"[COPY] {src} -> {dst}")

    def _cmd_move(self, src: str, dst: str) -> None:
        # TODO: conectar con biblioteca.filesystem.move(src, dst)
        print(f"[MOVE] {src} -> {dst}")

    def _cmd_delete(self, target: str) -> None:
        # TODO: conectar con biblioteca.filesystem.delete(target)
        print(f"[DELETE] {target}")

    def _cmd_makedir(self, path: str) -> None:
        # TODO: conectar con biblioteca.filesystem.makedir(path)
        print(f"[MAKEDIR] {path}")

    def _cmd_run(self, program: str) -> None:
        # TODO: conectar con biblioteca.system.run(program)
        print(f"[RUN] {program}")

    def _cmd_log(self, message: str) -> None:
        # TODO: conectar con biblioteca.logger.log(message)
        print(f"[LOG] {message}")


def execute(program: ProgramNode) -> Interpreter:
    """
    Helper opcional: ejecuta un programa y devuelve el intérprete
    (para inspeccionar las variables, etc.).
    """
    interp = Interpreter()
    interp.run(program)
    return interp
