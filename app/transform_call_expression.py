from app.inspector import Inspector
from app.syntax_node import SyntaxNode
from app.transform_on_next_semi import TransformOnNextSemi
from app.walk_tree import ITransformer, WalkTree


class TransformCallExpression(ITransformer):
    def __init__(self) -> None:
        self.next = TransformOnNextSemi()

    def transform(self, ctx: WalkTree, node: SyntaxNode):
        if not ctx.is_global():
            if node.type == 'call_expression':
                identifier = node.get(0, 'identifier')
                if identifier.text.startswith('inspector_'):
                    return

                self.next.nodes.append(Inspector.function_call(
                    node.line, node.column, ctx.function, identifier.text))
                self.next.nodes.append(SyntaxNode.mk(';'))
        self.next.transform(ctx, node)
