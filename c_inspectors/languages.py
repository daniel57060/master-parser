from tree_sitter import Language, Parser
from .resources import Resources
from .dependencies import ensure_dependencies

ensure_dependencies()

MY_LANGUAGUES_PATH = str(Resources.BUILD / 'my-languages.so')

Language.build_library(
    # Store the library in the `build` directory
    MY_LANGUAGUES_PATH,

    # Include one or more languages
    [
        str(Resources.VENDOR / 'tree-sitter-c'),
    ]
)

C_LANGUAGE = Language(MY_LANGUAGUES_PATH, 'c')


def c_parser():
    parser = Parser()
    parser.set_language(C_LANGUAGE)
    return parser
