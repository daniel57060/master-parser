from .inspector import Inspector
from .syntax_node import SyntaxNode
from .transform_on_next_semi import TransformOnNextSemi
from .walk_tree import ITransformer, WalkTree


class TransformVariableAssignment(ITransformer):
    def __init__(self):
        self.next = TransformOnNextSemi()

    def transform(self, ctx: WalkTree, node: SyntaxNode):
        if not ctx.is_global():
            if node.type == 'init_declarator' or node.type == 'assignment_expression':
                assert len(node.children) == 3
                identifier = node.get(0, 'identifier')
                v = ctx.variables.get_variable(identifier.text)

                self.next.nodes.append(Inspector.variable_assign(
                    node.line, node.column, ctx.function, v))
                self.next.nodes.append(SyntaxNode.mk(';'))
        self.next.transform(ctx, node)
