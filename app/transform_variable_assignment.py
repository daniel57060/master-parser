from app.inspector import Inspector
from app.syntax_node import SyntaxNode
from app.walk_tree import WalkTree


class TransformVariableAssignment:
    def __init__(self):
        self.nodes = []

    def transform(self, ctx: WalkTree, node: SyntaxNode):
        if not ctx.is_global():
            if node.type == 'init_declarator' or node.type == 'assignment_expression':
                assert len(node.children) == 3
                identifier = node.get(0, 'identifier')
                v = ctx.variables.get_variable(identifier.text)

                self.nodes.append(
                    Inspector.variable_assign(
                        node.line, node.column, ctx.function, v),
                )
                self.nodes.append(SyntaxNode.mk(';'))
            elif node.type == ';':
                if self.nodes:
                    node.type = '__sequence__'
                    node.text = None
                    node.children = [
                        SyntaxNode.mk(';'),
                        *self.nodes,
                    ]
                    self.nodes = []
