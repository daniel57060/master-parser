from .syntax_node import SyntaxNode
from .walk_tree import WalkTree

from .transform_add_inspector_headers import TransformAddInspectorHeaders
from .transform_function_into_inspector import TransformFunctionIntoInspector
from .transform_for_into_while import TransformForIntoWhile
from .transform_variable_declare import TransformVariableDeclare
from .transform_update_expression import TransformUpdateExpression
from .transform_conditions import TransformConditions
from .transform_variable_assignment import TransformVariableAssignment
from .transform_function_enter_exit import TransformFunctionEnterExit
from .transform_call_expression import TransformCallExpression


def transform_syntax_tree(syntax_tree: SyntaxNode):
    ctx = WalkTree()
    ctx.add_transformer(TransformAddInspectorHeaders())
    ctx.add_transformer(TransformFunctionIntoInspector())
    ctx.add_transformer(TransformForIntoWhile())
    ctx.add_transformer(TransformVariableAssignment())
    ctx.add_transformer(TransformCallExpression())
    ctx.add_transformer(TransformVariableDeclare())
    ctx.add_transformer(TransformUpdateExpression())
    ctx.add_transformer(TransformConditions())
    ctx.add_transformer(TransformFunctionEnterExit())
    ctx.walk(syntax_tree)
