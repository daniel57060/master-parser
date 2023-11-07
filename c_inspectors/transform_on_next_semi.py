
from .syntax_node import SyntaxNode
from .walk_tree import ITransformer, WalkTree


class TransformOnNextSemi(ITransformer):
    def __init__(self) -> None:
        self.nodes = []

    def transform(self, ctx: WalkTree, node: SyntaxNode):
        if not ctx.is_global():
            if node.type == ';':
                if self.nodes:
                    node.type = '__sequence__'
                    node.text = None
                    node.children = [SyntaxNode.mk(';'), *self.nodes,]
                    self.nodes = []
