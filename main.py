from typing import Optional
import json
from languages import c_parser

from app.resources import Resources
from app.walk_tree import WalkTree

from app.convert_json_to_str import convert_json_to_str
from app.convert_tree_to_json import convert_tree_to_json

from app.transform_add_inspector_headers import TransformAddInspectorHeaders
from app.transform_function_into_inspector import TransformFunctionIntoInspector
from app.transform_for_into_while import TransformForIntoWhile
from app.transform_variable_declare import TransformVariableDeclare
from app.transform_update_expression import TransformUpdateExpression
from app.transform_conditions import TransformConditions
from app.transform_variable_assignment import TransformVariableAssignment
from app.transform_function_enter_exit import TransformFunctionEnterExit


def process_sample(sample_name: str, sample_bytes: Optional[bytes] = None):
    print(f'Processing "{sample_name}"...')
    parser = c_parser()
    if sample_bytes is None:
        sample_bytes = Resources.get_sample(sample_name).read_bytes()

    tree = parser.parse(sample_bytes)

    json_result = convert_tree_to_json(tree)

    ctx = WalkTree()
    ctx.add_transformer(TransformAddInspectorHeaders())
    ctx.add_transformer(TransformFunctionIntoInspector())
    ctx.add_transformer(TransformForIntoWhile())
    ctx.add_transformer(TransformVariableAssignment())
    ctx.add_transformer(TransformVariableDeclare())
    ctx.add_transformer(TransformUpdateExpression())
    ctx.add_transformer(TransformConditions())
    ctx.add_transformer(TransformFunctionEnterExit())
    ctx.walk(json_result)

    with Resources.get_output(sample_name.replace('.c', '.json')).open('w') as f:
        json.dump(json_result.to_dict(), f, indent=2)

    sample_transformed = convert_json_to_str(json_result)
    with Resources.get_output(sample_name).open('w') as f:
        f.write(sample_transformed)


# fmt: off
# process_sample("empty.c")
# process_sample("only-fork-1.c")
# process_sample("only-fork-2.c")
# process_sample("only-fork-3.c")
# process_sample("program1.2.c")
# process_sample("program1.3.c")
# process_sample("program1.4.c")
# process_sample("program1.5.c")
# process_sample("program1.6.c")
# process_sample("program1.7.c")
# process_sample("program1.8.c")
# process_sample("program1.9.c")
# process_sample("program1.10.c")
# process_sample("program1.11.1.c")
# process_sample("program1.11.2.c")
# process_sample("program1.12.1.c")
# process_sample("program1.12.2.c")
# process_sample("program1.13.1.c")
# process_sample("program1.13.2.c")
# process_sample("program1.13.3.c")
# process_sample("program1.14.c")
# process_sample("for.c", (Resources.RESOURCES / "others" / "for.c").read_bytes())
process_sample("enter_exit.c", (Resources.RESOURCES / "others" / "enter_exit.c").read_bytes())
# process_sample("features.c", (Resources.RESOURCES / "others" / "features.c").read_bytes())
# process_sample("inspectors.c", (Resources.RESOURCES / "others" / "inspectors.c").read_bytes())
# fmt: on
