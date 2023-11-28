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
                if node.children[0].type in ['subscript_expression', 'array_declarator', 'pointer_declarator']:
                    # TODO(#0): ..\resources\outputs\c\array.json
                    return
                if node.children[0].type in ['field_expression']:
                    # TODO(#1): ..\resources\cpp-cheat\c\bitfield.c
                    return
                if node.children[0].type in ['pointer_declarator', 'pointer_expression', 'parenthesized_expression']:
                    # TODO(#5): ..\resources\cpp-cheat\c\const.c
                    return
                assert len(node.children) == 3
                identifier = node.get(0, 'identifier')
                v = ctx.variables.get_variable(identifier.text, fail=False)
                if v is None:
                    # TODO(#4): ..\resources\cpp-cheat\c\compound_literal.c
                    return

                self.next.nodes.append(Inspector.variable_assign(
                    node.line, node.column, ctx.function, v))
                self.next.nodes.append(SyntaxNode.mk(';'))
        self.next.transform(ctx, node)
