from .inspector import Inspector
from .syntax_node import SyntaxNode
from .transform_on_next_semi import TransformOnNextSemi
from .variable import Variable
from .walk_tree import ITransformer, WalkTree


class TransformVariableDeclare(ITransformer):
    def __init__(self) -> None:
        self.ctx = None
        self.variables = {}
        self.next = TransformOnNextSemi()

    def init(self, ctx: WalkTree):
        ctx.variables = self
        self.ctx = ctx

    def get_variable(self, name: str, *, fail=True) -> Variable:
        for scope in reversed(self.ctx.scopes):
            v_name = f'{scope}:{name}'
            v = self.variables.get(v_name)
            if v is not None:
                return v
        if not fail:
            return None
        print(self.variables)
        raise Exception(f'Variable "{name}" not found')

    def transform(self, ctx: WalkTree, node: SyntaxNode):
        if not ctx.is_global():
            if node.type == 'declaration':
                variable_type = node.children[0]

                vs: list[Variable] = []
                for it in node.children:
                    variable_name = None
                    if it.type == 'identifier':
                        variable_name = it
                    elif it.type == 'init_declarator':
                        if it.children[0].type in ['subscript_expression', 'array_declarator', 'pointer_declarator']:
                            # TODO(#0)
                            continue
                        variable_name = it.get(0, 'identifier')

                    if variable_name is not None:
                        vs.append(
                            Variable(variable_type.text, variable_name.text))

                scope = ctx.scope()
                for v in vs:
                    v_name = f'{scope}:{v.name}'
                    self.variables[v_name] = v

                    if node.children[-1].type != ';':
                        node.children.append(SyntaxNode.mk(';'))

                    self.next.nodes.append(
                        Inspector.variable_declare(node.line, node.column, ctx.function, v))
                    self.next.nodes.append(SyntaxNode.mk(';'))
        self.next.transform(ctx, node)
