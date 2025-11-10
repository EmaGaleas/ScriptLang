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

    def __repr__(self):
        return f'StringLiteralNode(value="{self.value}")'
    
class VariableRefNode(ExpressionNode):
    def __init__(self, name):
        #name: Nombre de la variable
        self.name = name

# Statement Nodes and Command Nodes
class AssignmentNode(StatementNode):
    def __init__(self, variable_name, value):
        # var_name: str (VAR)
        # value: StringLiteralNode
        self.variable_name = variable_name
        self.value = value

    def __repr__(self):
        return f'AssignmentNode(variable_name="{self.variable_name}", value={self.value})'
    
class CommandNode(StatementNode):
    """Base para nodos de comando (Copy, Move, Log, etc.)"""
    pass

class CopyCommandNode(CommandNode):
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination

    def __repr__(self):
        return f'CopyCommandNode(source={self.source}, destination={self.destination})'
    
class MoveCommandNode(CommandNode):
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination
    
class DeleteCommandNode(CommandNode):
    def __init__(self, target):
        self.target = target
        
    def __repr__(self):
        return f'DeleteCommandNode(target={self.target})'
        
class MakeDirCommandNode(CommandNode):
    def __init__(self, path):
        self.path = path
        
    def __repr__(self):
        return f'MakeDirCommandNode(path={self.path})'

    