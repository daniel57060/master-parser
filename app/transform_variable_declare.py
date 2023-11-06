from app.inspector import Inspector
from app.syntax_node import SyntaxNode
from app.variable import Variable
from app.walk_tree import WalkTree


class TransformVariableDeclare:
    def __init__(self) -> None:
        self.ctx = None
        self.variables = {}

    def init(self, ctx: WalkTree):
        ctx.variables = self
        self.ctx = ctx

    def get_variable(self, name: str) -> Variable:
        for scope in reversed(self.ctx.scopes):
            v_name = f'{scope}:{name}'
            v = self.variables.get(v_name)
            if v is not None:
                return v
        print(self.variables)
        raise Exception(f'Variable {name} not found')

    def transform(self, ctx: WalkTree, node: SyntaxNode):
        if not ctx.is_global():
            if node.type == 'declaration':
                variable_type = node.get(0, 'primitive_type')

                vs: list[Variable] = []
                for it in node.children:
                    variable_name = None
                    if it.type == 'identifier':
                        variable_name = it
                    elif it.type == 'init_declarator':
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

                    node.children.append(
                        Inspector.variable_declare(node.line, node.column, ctx.function, v))
                    node.children.append(SyntaxNode.mk(';'))
