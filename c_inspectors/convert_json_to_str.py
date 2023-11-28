
from .syntax_node import SyntaxNode


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
        '^', '|', '?', ':', '...', '\n', '.',
        '#define', '#include', '#if', '#ifdef', '#ifndef', '#endif',
        'typedef', 'sizeof', 
        'struct', 'union', 'enum',
        'for', 'while', 'do', 'if', 'else', 'goto', 'return', 
        'break', 'continue',
        'switch', 'case', 'default',
        'extern', 'static', 'auto', 'register', 'const', 'volatile',
        'unsigned']
    WRITE_TEXT = [
        '__lit__',
        'number_literal', 'string_literal', 'char_literal', 'identifier', 'type_identifier', 'field_identifier',
        'statement_identifier', 'primitive_type', 'system_lib_string', 'preproc_arg']
    GENERATE_CHILDREN = [
        '__sequence__',
        'storage_class_specifier',
        'sized_type_specifier',
        'compound_literal_expression',
        # struct
        'struct_specifier',
        'field_declaration_list',
        'field_declaration',
        'field_designator',
        'field_expression',
        'bitfield_clause',
        # root
        'root', 'translation_unit',
        # preproc
        'preproc_include',  'preproc_def',
        'preproc_if', 'preproc_ifdef', 'preproc_ifndef', 'preproc_endif',
        # type
        'type_descriptor', 'type_qualifier',
        # initializer
        'initializer_list', 'initializer_pair', 'subscript_designator',
        # abstract
        'abstract_pointer_declarator', 'abstract_array_declarator', 'abstract_parenthesized_declarator',
        # enum
        'enum_specifier', 'enumerator_list', 'enumerator',
        # function
        'function_definition',
        'function_declarator',
        'parameter_list',
        'parameter_declaration',
        # declaration
        'declaration', 'array_declarator',
        'init_declarator',
        'pointer_declarator',
        # statement
        'compound_statement', 'break_statement', 'expression_statement', 'if_statement', 'else_clause',
        'for_statement', 'while_statement', 'do_statement', 'goto_statement', 'return_statement',
        'labeled_statement', 'continue_statement', 'switch_statement', 'case_statement',
        # expression
        'assignment_expression', 'parenthesized_expression', 'binary_expression', 'unary_expression',
        'call_expression', 'argument_list', 'conditional_expression', 'pointer_expression',
        'comma_expression', 'update_expression', 'subscript_expression', 'sizeof_expression',
        'cast_expression',
    ]
    NO_SPACE_AFTER = {*GENERATE_CHILDREN, '++', '--', '&', '__lit__', '\n'}
    NEWLINE_AFTER = {'preproc_include', 'preproc_def', 'preproc_ifdef', 'preproc_ifndef', 'preproc_endif'}

    def __init__(self, writer: IWritable):
        self.writer = writer
        self.identation = 0

    def _unimplemented(self, node: SyntaxNode):
        print(node)
        print([it.type for it in node.children])
        raise NotImplementedError(f"Unimplemented: {repr(node.type)}")

    def _generate_children(self, node: SyntaxNode):
        for child in node.children:
            self.generate(child)

    def _write_identation(self):
        if self.identation > 0:
            self.writer.write('  ' * self.identation)

    def _before_node(self, node: SyntaxNode):
        if node.type == '{':
            self.writer.write('\n')
            self._write_identation()
            self.identation += 1
        if node.type == '}':
            self.writer.write('\n')
            self.identation -= 1
            self._write_identation()

    def _after_node(self, node: SyntaxNode):
        if node.type not in G.NO_SPACE_AFTER:
            self.writer.write(' ')

        if node.type in G.NEWLINE_AFTER:
            self.writer.write('\n')

        if node.type == '{':
            # self.identation += 1
            self.writer.write('\n')
            self._write_identation()
        if node.type == '}':
            # self.identation -= 1
            self.writer.write('\n')
            self._write_identation()
        if node.type == ';':
            self.writer.write('\n')
            self._write_identation()

    def generate(self, node: SyntaxNode) -> str:
        self._before_node(node)

        if node.type in G.WRITE_TEXT:
            if node.text is None:
                self._unimplemented(node)
            self.writer.write(node.text)
        elif node.type in G.WRITE_TYPE:
            if node.type is None:
                self._unimplemented(node)
            self.writer.write(node.type)
        elif node.type in G.GENERATE_CHILDREN:
            self._generate_children(node)
        elif node.type == 'comment':
            pass
        elif node.type == 'null':
            self.writer.write(node.children[0].type)
        else:
            self._unimplemented(node)

        self._after_node(node)


def convert_json_to_str(root: SyntaxNode) -> str:
    w = WriteableStr()
    G(w).generate(root)
    return w.to_str()
