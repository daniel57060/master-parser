from tree_sitter import Node, Tree

from app.syntax_node import SyntaxNode

no_collect_text = [
    "root", "translation_unit",

    "function_definition", "function_declarator",

    'compound_statement', 'break_statement', 'expression_statement', 'if_statement',
    'for_statement', 'while_statement', 'do_statement', 'goto_statement', 'return_statement',
    'labeled_statement', 'continue_statement', 'switch_statement', 'case_statement',

    "call_expression",
]
collect_text = ["system_lib_string", "primitive_type", "identifier",
                "number_literal", "string_literal", "character_literal",
                "type_identifier", "comment", "statement_identifier", "preproc_arg"]


def json_from_node(node: Node):
    return SyntaxNode(
        type=node.type,
        line=node.start_point[0],
        column=node.start_point[1],
        text=node.text.decode() if node.type not in no_collect_text else None,
        children=[],
    )


def convert_tree_to_json(tree: Tree) -> SyntaxNode:
    json = json_from_node(tree.root_node)
    json.type = "root"
    stack = [(tree.root_node, json)]

    while stack:
        (current_node, current_json) = stack.pop()
        current_json.children.append(json_from_node(current_node))

        if hasattr(current_node, 'children'):
            for child in reversed(current_node.children):
                stack.append((child, current_json.children[-1]))

    return json
