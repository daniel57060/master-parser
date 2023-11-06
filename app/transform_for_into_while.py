from app.syntax_node import SyntaxNode, compound_statement_into_do_while, mk_compound_statement, wrap_in_parenthesized_expression
from app.walk_tree import ITransformer, WalkTree


class TransformForIntoWhile(ITransformer):
    def transform(self, ctx: WalkTree, node: SyntaxNode):
        if node.type == 'for_statement':
            self._change_for_statement(node)
            self._change_for_body(node)
            self._change_for_declaration(node)

    def _change_for_statement(self, node: SyntaxNode):
        semi_count = len(node.children)
        if semi_count == 9:
            # Ok
            pass
        elif semi_count == 8:
            assert node.children[2].children[-1].type == ';'
            node.children[2].children.pop()
            node.children.insert(3, SyntaxNode.mk(';'))
        else:
            raise Exception('Invalid for statement')
        return node

    def _change_for_body(self, node: SyntaxNode):
        semi_count = len(node.children)
        if semi_count == 9:
            maybe_compound_statment = node.children[-1]
            if maybe_compound_statment.type == 'compound_statement':
                node.children[-1] = compound_statement_into_do_while(
                    maybe_compound_statment)
        else:
            raise Exception('Invalid for statement')

    def _change_for_declaration(self, node: SyntaxNode):
        semi_count = len(node.children)
        if semi_count == 9:
            init_statement = node.children[2]
            condition_expression = node.children[4]
            increment_expression = node.children[6]
            body_statement = node.children[8]

            condition_expression = wrap_in_parenthesized_expression(
                condition_expression)

            body_statement = mk_compound_statement(body_statement)
            body_statement.children = [
                SyntaxNode.mk('{'),
                body_statement.shallow_copy(),
                increment_expression,
                SyntaxNode.mk(';'),
                SyntaxNode.mk('}'),
            ]

            while_statement = node.shallow_copy()
            while_statement.type = 'while_statement'
            while_statement.children = [
                SyntaxNode.mk('while'),
                condition_expression,
                body_statement,
            ]

            node.type = 'compound_statement'
            node.children = [
                SyntaxNode.mk('{'),
                init_statement.shallow_copy(),
                SyntaxNode.mk(';'),
                while_statement,
                SyntaxNode.mk('}'),
            ]
        else:
            raise Exception('Invalid for statement')
