from app.inspector import Inspector
from app.syntax_node import SyntaxNode
from app.walk_tree import ITransformer, WalkTree


class TransformFunctionIntoInspector(ITransformer):
    def transform(self, ctx: WalkTree, node: SyntaxNode):
        if not ctx.is_global():
            if node.type == 'call_expression':
                function_name = node.get(0, 'identifier')
                if function_name.text in Inspector.FUNCTIONS:
                    self._transform_function_into_inspector(ctx.function, node)

    def _transform_function_into_inspector(self, function_call_name: str, node: SyntaxNode):
        function_name = node.get(0, 'identifier')
        argument_list = node.get(1, 'argument_list')
        inspector_function = Inspector.inspect_function(
            function_name.text, node.line, node.column, function_call_name,
            [it for it in argument_list.children[1:-1] if it.type != ','])
        node.assign(inspector_function)
