from app.syntax_node import SyntaxNode
from collections import deque


class ITransformer:
    def transform(self, ctx: 'WalkTree', node: SyntaxNode):
        raise NotImplementedError()


class WalkTree:
    def __init__(self) -> None:
        self.function = None
        self.parents = []
        self.transformers = []

        self.parentesis_count = 0
        self.scope_count = 0
        self.scopes = ['global()']

    def add_transformer(self, transformer: 'ITransformer'):
        self.transformers.append(transformer)

    def is_global(self):
        return self.function is None

    def scope(self):
        return self.scopes[-1]

    def function_enter(self):
        return len(self.parents) == 4 and self.parents[2].type == 'function_definition'

    def function_exit(self):
        return len(self.parents) == 4

    def _look(self, node: SyntaxNode, parents: SyntaxNode):
        self.parents = parents

        if node.type == '{':
            if self.function_enter():
                assert self.parents[3].type == 'compound_statement'
                function_name = self.parents[2].get(1, 'function_declarator')
                function_name = function_name.get(0, 'identifier')
                self.function = function_name.text
            self.scope_count += 1
            self.parentesis_count += 1
            self.scopes.append(
                f'{self.function or "global()"}:{self.scope_count}')

        for transformer in self.transformers:
            transformer.transform(self, node)

        if node.type == '}':
            self.parentesis_count -= 1
            if self.parentesis_count == 0:
                self.function = None

    def ignore(self, child: SyntaxNode):
        return any([
            child.type == '__lit__',
            child.type == '__inspector__',
        ])

    def walk(self, root: SyntaxNode):
        for transformer in self.transformers:
            if hasattr(transformer, 'init'):
                transformer.init(self)

        walk_tree(root, self)


def walk_tree(root: SyntaxNode, ctx: WalkTree) -> None:
    stack = deque([(root, [])])
    while stack:
        node, parents = stack.pop()
        ctx._look(node, parents)

        for child in reversed(node.children):
            if ctx.ignore(child):
                continue

            if child.type == 'compound_statement':
                stack.append((child, parents + [node]))
            else:
                stack.append((child, parents + [node]))
