from typing import Any
from app.parse_and_transform_file import ParserAndTransformFile
from app.dependencies import ensure_dependencies
from pathlib import Path

import argparse


class Cli:
    @staticmethod
    def get_argument_parser():
        def type_path(*, required=False):
            def _type_path(path_str: str):
                filepath = Path(path_str)
                if required and not filepath.exists():
                    raise argparse.ArgumentTypeError(
                        f'File "{filepath}" does not exist')
                return filepath
            return _type_path

        parser = argparse.ArgumentParser()

        parser.add_argument('input_path', type=type_path(required=True),
                            help='The c input file path')
        parser.add_argument('output_path', type=type_path(),
                            help='The c output file path')
        parser.add_argument('--json_path', type=type_path(), default=None,
                            help='The json output file path')
        parser.add_argument('--silent', action='store_true',
                            help='Disable logging')

        return parser

    @staticmethod
    def execute(args: Any):
        ParserAndTransformFile(
            input_path=args.input_path,
            output_path=args.output_path,
            json_path=args.json_path,
            log=not args.silent
        ).run()

    @staticmethod
    def run():
        ensure_dependencies()
        parser = Cli.get_argument_parser()
        args = parser.parse_args()
        Cli.execute(args)
