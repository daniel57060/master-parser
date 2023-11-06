from app.inspector import Inspector
from app.syntax_node import SyntaxNode
from app.walk_tree import WalkTree


class TransformFunctionEnterExit:
    def transform(self, ctx: WalkTree, node: SyntaxNode):
        if node.type == '{' and ctx.function_enter():
            self._transform_enter(ctx, node)
        elif node.type == '}' and ctx.function_exit():
            self._transform_exit(ctx, node)

    def _transform_enter(self, ctx: WalkTree, node: SyntaxNode):
        node.type = '__sequence__'
        node.text = None
        node.children = [
            SyntaxNode.mk('{'),
            Inspector.function_enter(
                node.line, node.column, ctx.function),
            SyntaxNode.mk(';'),
        ]

    def _transform_exit(self, ctx: WalkTree, node: SyntaxNode):
        parent = ctx.parents[-1]
        if parent.children[-2].type == 'return_statement':
            parent.children.insert(-2, Inspector.function_exit(
                node.line, node.column, ctx.function))
            parent.children.insert(-2, SyntaxNode.mk(';'))
        else:
            node.type = '__sequence__'
            node.text = None
            node.children = [
                Inspector.function_exit(
                    node.line, node.column, ctx.function),
                SyntaxNode.mk(';'),
                SyntaxNode.mk('}'),
            ]
