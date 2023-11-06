
from app.syntax_node import SyntaxNode


class IWritable:
    def write(self, s: str):
        ...

    def to_str(self) -> str:
        ...


class WriteableStr(IWritable):
    def __init__(self):
        self.parts = []

    def write(self, s: str):
        self.parts.append(s)

    def to_str(self) -> str:
        return ''.join(self.parts)


class G:
    WRITE_TYPE = [
        '++', '--', '&', '[', ']', '(', ')', '{', '}', ';', ',', '->', '==', '!=',
        '>', '<', '>=', '<=', '+', '-', '*', '/', '%', '!', '&&', '||', '=', '+=',
        '-=', '*=', '/=', '%=', '<<', '>>', '&=', '|=', '^=', '<<=', '>>=', '~',
        '^', '|', '?', ':', '...', 'sizeof', 'for', 'while', 'do', 'if', 'else',
        'goto', 'return', '#define', '#include', 'typedef', 'struct', 'union',
        'enum', 'break', 'continue', 'switch', 'case', 'default', 'extern']
    WRITE_TEXT = [
        '__lit__',
        'number_literal', 'string_literal', 'identifier', 'type_identifier',
        'statement_identifier', 'primitive_type', 'system_lib_string', 'preproc_arg']
    GENERATE_CHILDREN = [
        '__sequence__',
        # root
        'root', 'translation_unit',
        # preproc
        'preproc_include',  'preproc_def',
        # function
        'function_definition',
        'function_declarator',
        'parameter_list',
        'parameter_declaration',
        # declaration
        'declaration', 'array_declarator',
        'init_declarator',
        # statement
        'compound_statement', 'break_statement', 'expression_statement', 'if_statement',
        'for_statement', 'while_statement', 'do_statement', 'goto_statement', 'return_statement',
        'labeled_statement', 'continue_statement', 'switch_statement', 'case_statement',
        # expression
        'assignment_expression', 'parenthesized_expression', 'binary_expression', 'unary_expression',
        'call_expression', 'argument_list', 'conditional_expression', 'pointer_expression',
        'comma_expression', 'update_expression']
    NO_SPACE_AFTER = {*GENERATE_CHILDREN, '++', '--', '&', '__lit__'}
    NEWLINE_AFTER = {'preproc_include', 'preproc_def'}

    def __init__(self, writer: IWritable):
        self.writer = writer

    def _unimplemented(self, node: SyntaxNode):
        print(node)
        print([it.type for it in node.children])
        raise NotImplementedError(f"Unimplemented: {repr(node.type)}")

    def _generate_children(self, node: SyntaxNode, ident=0):
        for child in node.children:
            self.generate(child, ident)

    def _write_ident(self, ident: int):
        self.writer.write('  ' * ident)

    def _before_node(self, node: SyntaxNode, ident: int):
        pass

    def _after_node(self, node: SyntaxNode, ident: int):
        if node.type not in G.NO_SPACE_AFTER:
            self.writer.write(' ')

        if node.type in G.NEWLINE_AFTER:
            self.writer.write('\n')

    def generate(self, node: SyntaxNode, ident=0) -> str:
        self._before_node(node, ident)

        if node.type in G.WRITE_TEXT:
            if node.text is None:
                self._unimplemented(node)
            self.writer.write(node.text)
        elif node.type in G.WRITE_TYPE:
            if node.type is None:
                self._unimplemented(node)
            self.writer.write(node.type)
        elif node.type in G.GENERATE_CHILDREN:
            self._generate_children(node, ident)
        elif node.type == 'comment':
            pass
        elif node.type == 'null':
            self.writer.write(node.children[0].type)
        else:
            self._unimplemented(node)

        self._after_node(node, ident)


def convert_json_to_str(root: SyntaxNode) -> str:
    w = WriteableStr()
    G(w).generate(root)
    return w.to_str()
