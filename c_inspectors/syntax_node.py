
from dataclasses import dataclass
from typing import Optional, List


@dataclass
class SyntaxNode:
    type: str
    line: int
    column: int
    text: Optional[str]
    children: list['SyntaxNode']

    @staticmethod
    def mk(node_type: str, **kargs):
        node = SyntaxNode(node_type, 0, 0, None, [])
        for key, value in kargs.items():
            setattr(node, key, value)
        return node

    @staticmethod
    def literal(text: str, node_type="__lit__"):
        return SyntaxNode(node_type, 0, 0, text, [])

    def assign(self, other: 'SyntaxNode'):
        self.type = other.type
        self.line = other.line
        self.column = other.column
        self.text = other.text
        self.children = other.children

    def to_dict_iterative(self):
        # TODO: check if the function performs the same as the recursive version
        root = self.to_dict0()
        stack = [(self, root)]
        while stack:
            node, node_j = stack.pop()
            for child in node.children:
                child_j = child.to_dict0()
                node_j['children'].append(child_j)
                stack.append((child, child_j))
        return root

    def to_dict(self):
        return {
            'type': self.type,
            'line': self.line,
            'column': self.column,
            'text': self.text,
            'children': [child.to_dict() for child in self.children],
        }

    def to_dict0(self):
        return {
            'type': self.type,
            'line': self.line,
            'column': self.column,
            'text': self.text,
            'children': [],
        }

    def shallow_copy(self):
        return SyntaxNode(
            type=self.type,
            line=self.line,
            column=self.column,
            text=self.text,
            children=[child for child in self.children],
        )

    def get(self, index: int, child_type: str):
        if len(self.children) <= index:
            raise Exception(f"Expected {child_type}, got nothing")

        if self.children[index].type != child_type:
            raise Exception(
                f"Expected {child_type}, got {self.children[index].type}")

        return self.children[index]

    def find(self, child_type: str, *, fail=True):
        for child in self.children:
            if child.type == child_type:
                return child
            node = child.find(child_type, fail=False)
            if node is not None:
                return node
        if not fail:
            return None
        raise Exception(f"Expected {child_type}, got nothing")

    def children_types(self):
        return [child.type for child in self.children]

    def __str__(self):
        if self.text:
            return f"{self.text}"
        elif self.children:
            return '[' + ', '.join(['"' + str(it) + '"' for it in self.children]) + ']'
        else:
            return f"{self.type}"


def sep_nodes_by(nodes: List[SyntaxNode], sep: SyntaxNode) -> List[SyntaxNode]:
    result = []
    for i, node in enumerate(nodes):
        if i > 0:
            result.append(sep.shallow_copy())
        result.append(node)
    return result


def mk_call_expression(function_name: str, argument_list: List[SyntaxNode]) -> SyntaxNode:
    return SyntaxNode.mk('call_expression', children=[
        SyntaxNode.mk('identifier', text=function_name),
        SyntaxNode.mk('('),
        *sep_nodes_by(argument_list, SyntaxNode.mk(',')),
        SyntaxNode.mk(')'),
    ])


def mk_compound_statement(node: SyntaxNode) -> SyntaxNode:
    return SyntaxNode.mk('compound_statement', children=[
        SyntaxNode.mk('{'),
        node,
        SyntaxNode.mk('}'),
    ])


def wrap_in_parenthesized_expression(node: SyntaxNode) -> SyntaxNode:
    parenthesized_expression = node.shallow_copy()
    parenthesized_expression.type = 'parenthesized_expression'
    parenthesized_expression.children = [
        SyntaxNode.mk('('),
        node.shallow_copy(),
        SyntaxNode.mk(')'),
    ]
    return parenthesized_expression


def compound_statement_into_do_while(compound_statement: SyntaxNode):
    assert compound_statement.type == 'compound_statement'

    parenthesized_expression = wrap_in_parenthesized_expression(
        SyntaxNode.literal('0', 'number_literal'))

    do_statement = compound_statement.shallow_copy()
    do_statement.type = 'do_statement'
    do_statement.children = [
        SyntaxNode.mk('do'),
        compound_statement,
        SyntaxNode.mk('while'),
        parenthesized_expression,
        SyntaxNode.mk(';'),
    ]
    return do_statement
