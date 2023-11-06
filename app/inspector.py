from .syntax_node import SyntaxNode, mk_call_expression
from .variable import Variable


class Inspector:
    FUNCTIONS = ['wait', 'waitpid', 'fork', 'printf', 'exit']

    @staticmethod
    def function_enter(line, col, function_name):
        return Inspector.inspect_function('function_enter', line, col, function_name, [])

    @staticmethod
    def function_exit(line, col, function_name):
        return Inspector.inspect_function('function_exit', line, col, function_name, [])

    @staticmethod
    def function_call(line, col, function_caller_name, function_name):
        return Inspector.inspect_function('function_call', line, col, function_caller_name, [
            SyntaxNode.mk('string_literal', text=f'"{function_name}"'),
        ])

    @staticmethod
    def variable_declare(line, col, function_name, v: Variable):
        return Inspector.inspect_function('variable_declare', line, col, function_name, [
            SyntaxNode.mk('string_literal', text=f'"{v.type}"'),
            SyntaxNode.mk('string_literal', text=f'"{v.name}"'),
        ])

    @staticmethod
    def variable_assign(line, col, function_name, v: Variable):
        return Inspector.inspect_function('variable_assign', line, col, function_name, [
            SyntaxNode.mk('string_literal', text=f'"{v.type}"'),
            SyntaxNode.mk('string_literal', text=f'"{v.name}"'),
            SyntaxNode.mk('pointer_expression', children=[
                SyntaxNode.mk('&'),
                SyntaxNode.mk('identifier', text=v.name),
            ])
        ])

    @staticmethod
    def condition(line, col, function_name, cause, condition):
        return Inspector.inspect_function('condition', line, col, function_name, [
            SyntaxNode.mk('string_literal', text=f'"{cause}"'),
            condition,
            SyntaxNode.mk('string_literal', text=f'"{condition.text}"'),
        ])

    @staticmethod
    def inspect_function(name, line, col, function_name, args):
        return mk_call_expression(f'inspector_{name}', [
            SyntaxNode.mk('string_literal', text=f'"{function_name}"'),
            SyntaxNode.mk('number_literal', text=f'{line}'),
            *args,
        ])
