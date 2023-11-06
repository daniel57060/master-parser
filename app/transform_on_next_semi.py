
from app.inspector import Inspector
from app.syntax_node import SyntaxNode
from app.walk_tree import WalkTree


class TransformOnNextSemi:
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
