# Crear estructura de nodos del AST (por ejemplo: CommandNode, ArgumentNode).
# Se añaden tambien los métodos __repr__ para facilitar la depuración e impresión de los nodos.
class ASTNode:
    """Nodo base para el AST."""
    pass

# Base Node and Root Node
class ProgramNode(ASTNode):
    def __init__(self, statements):
        #statements: lista de StatementNode
        self.statements = statements
    
    # optional: program-level position could be added later

class StatementNode(ASTNode):
    """Base para asignacion de comandos"""
    pass

class ExpressionNode(ASTNode):
    """Base para expresiones"""
    pass

# Expression Nodes
class StringLiteralNode(ExpressionNode):
    def __init__(self, value):
        #value: El contenido del string, que puede incluir referencias a variables
        self.value = value
        self.line = None
        self.column = None

    def set_pos(self, token):
        if token is None:
            return
        self.line = getattr(token, 'line', None)
        self.column = getattr(token, 'column', None)

    def __repr__(self):
        return f'StringLiteralNode(value="{self.value}")'
    
class VariableRefNode(ExpressionNode):
    def __init__(self, name):
        #name: Nombre de la variable
        self.name = name
        self.line = None
        self.column = None

    def set_pos(self, token):
        if token is None:
            return
        self.line = getattr(token, 'line', None)
        self.column = getattr(token, 'column', None)

# Statement Nodes and Command Nodes
class AssignmentNode(StatementNode):
    def __init__(self, variable_name, value):
        # var_name: str (VAR)
        # value: StringLiteralNode
        self.variable_name = variable_name
        self.value = value

    def __repr__(self):
        return f'AssignmentNode(variable_name="{self.variable_name}", value={self.value})'
    
    def set_pos(self, token):
        self.line = getattr(token, 'line', None) if token is not None else None
        self.column = getattr(token, 'column', None) if token is not None else None
    
class CommandNode(StatementNode):
    """Base para nodos de comando (Copy, Move, Log, etc.)"""
    pass

class CopyCommandNode(CommandNode):
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination

        self.line = None
        self.column = None

    def set_pos(self, token):
        if token is None:
            return
        self.line = getattr(token, 'line', None)
        self.column = getattr(token, 'column', None)

    def __repr__(self):
        return f'CopyCommandNode(source={self.source}, destination={self.destination})'
    
class MoveCommandNode(CommandNode):
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination
        self.line = None
        self.column = None

    def set_pos(self, token):
        if token is None:
            return
        self.line = getattr(token, 'line', None)
        self.column = getattr(token, 'column', None)
    
class DeleteCommandNode(CommandNode):
    def __init__(self, target):
        self.target = target
        self.line = None
        self.column = None

    def set_pos(self, token):
        if token is None:
            return
        self.line = getattr(token, 'line', None)
        self.column = getattr(token, 'column', None)
    def __repr__(self):
        return f'DeleteCommandNode(target={self.target})'
        
class MakeDirCommandNode(CommandNode):
    def __init__(self, path):
        self.path = path
        self.line = None
        self.column = None

    def set_pos(self, token):
        if token is None:
            return
        self.line = getattr(token, 'line', None)
        self.column = getattr(token, 'column', None)
    def __repr__(self):
        return f'MakeDirCommandNode(path={self.path})'
    
class RunCommandNode(CommandNode):
    def __init__(self, program):
        self.program = program 
        self.line = None
        self.column = None

    def set_pos(self, token):
        if token is None:
            return
        self.line = getattr(token, 'line', None)
        self.column = getattr(token, 'column', None)

class LogCommandNode(CommandNode):
    def __init__(self, message):
        self.message = message     
        self.line = None
        self.column = None

    def set_pos(self, token):
        if token is None:
            return
        self.line = getattr(token, 'line', None)
        self.column = getattr(token, 'column', None)

# C. Estructura de Control
class ExistsConditionNode(ASTNode):
    def __init__(self, path):
        self.path = path
        self.line = None
        self.column = None

    def set_pos(self, token):
        if token is None:
            return
        self.line = getattr(token, 'line', None)
        self.column = getattr(token, 'column', None)

class IfStatementNode(StatementNode):
    def __init__(self, condition, if_body, else_body=None):
        self.condition = condition    # ExistsConditionNode
        self.if_body = if_body        # list[StatementNode]
        self.else_body = else_body    # list[StatementNode] o None
        self.line = None
        self.column = None

    def set_pos(self, token):
        if token is None:
            return
        self.line = getattr(token, 'line', None)
        self.column = getattr(token, 'column', None)

    def __repr__(self):
        return f'IfStatementNode(condition={self.condition}, if_body={self.if_body}, else_body={self.else_body})'