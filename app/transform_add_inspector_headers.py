from .syntax_node import SyntaxNode
from .walk_tree import ITransformer, WalkTree


class TransformAddInspectorHeaders(ITransformer):
    def transform(self, ctx: WalkTree, node: SyntaxNode):
        if node.type == 'root':
            node.children = [
                SyntaxNode.literal('#define INSPECTOR_IMPLEMENTATION\n'),
                SyntaxNode.literal('#include <inspector.h>\n'),
                *node.children,
            ]
