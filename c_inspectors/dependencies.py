from subprocess import run

from .resources import Resources


def ensure_dependencies():
    git_dependencies = [
        ('tree-sitter-c', 'https://github.com/tree-sitter/tree-sitter-c.git')
    ]

    for name, url in git_dependencies:
        path_name = Resources.VENDOR / name
        if not path_name.exists():
            print(f'Cloning {url}...')
            run(['git', 'clone', '--depth=1', url, str(path_name)], check=True)
