from app.inspector import Inspector
from app.syntax_node import SyntaxNode
from app.walk_tree import ITransformer, WalkTree


class TransformUpdateExpression(ITransformer):
    def transform(self, ctx: WalkTree, node: SyntaxNode):
        if not ctx.is_global():
            if node.type == 'update_expression':
                assert len(node.children) == 2
                identifier = node.find('identifier')
                v = ctx.variables.get_variable(identifier.text)

                node.children = [
                    SyntaxNode.mk('('),
                    SyntaxNode.literal(node.text),
                    SyntaxNode.mk(','),
                    Inspector.variable_assign(
                        node.line, node.column, ctx.function, v),
                    SyntaxNode.mk(','),
                    identifier,
                    SyntaxNode.mk(')'),
                ]
