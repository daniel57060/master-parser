from app.inspector import Inspector
from app.syntax_node import SyntaxNode, wrap_in_parenthesized_expression
from app.walk_tree import ITransformer, WalkTree


class TransformConditions(ITransformer):
    def transform(self, ctx: WalkTree, node: SyntaxNode):
        if node.type == 'if_statement':
            self._change_expression('if', ctx, node, 1)
        elif node.type == 'while_statement':
            self._change_expression('while', ctx, node, 1)
        elif node.type == 'do_statement':
            node.get(0, 'do')
            node.get(2, 'while')
            parenthesized_expression = node.get(3, 'parenthesized_expression')
            value = parenthesized_expression.children[1]
            process = True
            if value.type == 'number_literal' and value.text == '0':
                process = False
            if process:
                self._change_expression('do', ctx, node, 3)

    def _change_expression(self, cause: str, ctx: WalkTree, node: SyntaxNode, index: int):
        node.get(0, cause)
        parenthesized_expression = node.get(index, 'parenthesized_expression')
        parenthesized_expression.children = parenthesized_expression.children[1:-1]
        parenthesized_expression.text = parenthesized_expression.text[1:-1]
        parenthesized_expression = Inspector.condition(
            node.line, node.column, ctx.function, cause, parenthesized_expression)
        node.children[1] = wrap_in_parenthesized_expression(
            parenthesized_expression)
