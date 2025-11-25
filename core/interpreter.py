# core/interpreter.py
from __future__ import annotations
from typing import Dict, List
from biblioteca import filesystem, system, logger as std_logger

from core.ast_nodes import (
    ProgramNode, AssignmentNode, CopyCommandNode, StatementNode, MoveCommandNode, ExpressionNode,
    DeleteCommandNode, MakeDirCommandNode, RunCommandNode, LogCommandNode,
    IfStatementNode, ExistsConditionNode, StringLiteralNode, VariableRefNode,
)
from core import semantic

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
        Verifica la condición EXISTS(path) delegando a biblioteca.filesystem.exists.
        Devolver False y loggear si hay error.
        """
        # Bloquear rutas vacías por seguridad
        if not path or not path.strip():
            std_logger.log_warning("EXISTS recibido con ruta vacía.")
            return False
        try:
            return filesystem.exists(path)
        except Exception as e:
            std_logger.log_error(f"Error en EXISTS('{path}'): {e}", exc_info=True)
            return False

    # === Handlers de comandos (implementados con biblioteca) ===

    def _cmd_copy(self, src: str, dst: str) -> None:
        # validaciones básicas
        if not src or not src.strip():
            raise InterpreterError("Ruta de origen vacía no permitida.")
        if not dst or not dst.strip():
            raise InterpreterError("Ruta destino vacía no permitida.")

        try:
            filesystem.copy(src, dst)
            std_logger.log_info(f"COPY: {src} -> {dst}")
        except Exception as e:
            std_logger.log_error(f"Error copy {src} -> {dst}: {e}", exc_info=True)
            raise InterpreterError(f"Error al copiar: {e}")

    def _cmd_move(self, src: str, dst: str) -> None:
        if not src or not src.strip():
            raise InterpreterError("Ruta de origen vacía no permitida.")
        if not dst or not dst.strip():
            raise InterpreterError("Ruta destino vacía no permitida.")

        try:
            filesystem.move(src, dst)
            std_logger.log_info(f"MOVE: {src} -> {dst}")
        except Exception as e:
            std_logger.log_error(f"Error move {src} -> {dst}: {e}", exc_info=True)
            raise InterpreterError(f"Error al mover: {e}")

    def _cmd_delete(self, target: str) -> None:
        if not target or not target.strip():
            raise InterpreterError("Ruta vacía no permitida para delete.")

        try:
            filesystem.delete(target)
            std_logger.log_info(f"DELETE: {target}")
        except Exception as e:
            std_logger.log_error(f"Error delete {target}: {e}", exc_info=True)
            raise InterpreterError(f"Error al borrar: {e}")

    def _cmd_makedir(self, path: str) -> None:
        if not path or not path.strip():
            raise InterpreterError("Ruta vacía no permitida para makedir.")
        try:
            filesystem.makedir(path)
            std_logger.log_info(f"MAKEDIR: {path}")
        except Exception as e:
            std_logger.log_error(f"Error makedir {path}: {e}", exc_info=True)
            raise InterpreterError(f"Error al crear directorio: {e}")

    def _cmd_run(self, program: str) -> None:
        if not program or not program.strip():
            raise InterpreterError("Comando vacío no permitido.")

        try:
            # Por seguridad: shell=False por defecto. Si quieres permitir shell features, cambia shell=True.
            rc, out, err = system.run(program, capture_output=True, shell=False)
            std_logger.log_info(f"RUN: {program} rc={rc}")
            if out:
                std_logger.log_info(f"RUN stdout: {out.strip()}")
            if err:
                std_logger.log_error(f"RUN stderr: {err.strip()}")

            if rc != 0:
                raise InterpreterError(f"Comando '{program}' finalizó con código {rc}")
        except InterpreterError:
            raise
        except Exception as e:
            std_logger.log_error(f"Error run {program}: {e}", exc_info=True)
            raise InterpreterError(f"Error al ejecutar comando: {e}")

    def _cmd_log(self, message: str) -> None:
        try:
            std_logger.log_info(message)
        except Exception as e:
            # No detener ejecución por fallo de logging; imprimir en consola como fallback
            print(f"[LOG ERROR] {e}")

def execute(program: ProgramNode) -> Interpreter:
    """
    Helper: ejecuta un programa y devuelve el intérprete.
    Inicializa el logger por defecto (scriptlang.log).
    """
    # Primero: comprobar semántica y bloquear ejecución si hay errores.
    semantic.check(program)

    # Inicializa logger por defecto (archivo scriptlang.log en cwd)
    std_logger.init_logger("scriptlang.log", level="INFO")
    interp = Interpreter()
    interp.run(program)
    return interp
