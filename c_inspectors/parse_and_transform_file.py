from dataclasses import dataclass
import json
from pathlib import Path
from typing import Optional

from .convert_json_to_str import convert_json_to_str
from .convert_tree_to_json import convert_tree_to_json
from .languages import c_parser
from .resources import Resources
from .transform_syntax_tree import transform_syntax_tree

LOG = False

parser = c_parser()


@dataclass
class ParserAndTransformFile:
    input_path: Path
    output_path: Path
    json_path: Optional[Path]
    log: bool = False

    def run(self):
        if self.log:
            self.enable_log()
        parse_and_transform_file(self)

    def enable_log(self):
        enable_log()
        return self


def parse_and_transform_file(args: ParserAndTransformFile):
    log(f'INFO: Parsing and transforming "{simple_path(args.input_path)}"')
    content = args.input_path.read_bytes()
    tree = parser.parse(content)
    json_result = convert_tree_to_json(tree)
    
    if args.json_path is not None:
        log(f'INFO: Saving json to "{simple_path(args.json_path)}"')
        with args.json_path.open('w') as f:
            json.dump(json_result.to_dict(), f, indent=2)

    transform_syntax_tree(json_result)

    if args.json_path is not None:
        log(f'INFO: Saving json to "{simple_path(args.json_path)}"')
        with args.json_path.open('w') as f:
            json.dump(json_result.to_dict(), f, indent=2)

    log(f'INFO: Saving transformed to "{simple_path(args.output_path)}"')
    sample_transformed = convert_json_to_str(json_result)
    with args.output_path.open('w') as f:
        f.write(sample_transformed)


def simple_path(path: Path):
    root = str(Resources.ROOT) + "\\"
    return str(path).replace(root, "")


def log(*args):
    if LOG:
        print(*args)


def enable_log():
    global LOG
    LOG = True
