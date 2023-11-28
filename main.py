from pathlib import Path

from c_inspectors.resources import Resources

from c_inspectors.parse_and_transform_file import ParserAndTransformFile


def run(input_path: Path):
    outdir = Resources.OUTPUTS / input_path.parent.name
    outdir.mkdir(parents=True, exist_ok=True)

    json_path = outdir / input_path.with_suffix(".json").name
    output_path = outdir / input_path.with_suffix(".out.c").name
    ParserAndTransformFile(input_path=input_path, output_path=output_path, json_path=json_path).enable_log().run()
    print()


# fmt: off
# print("INFO: Running samples\n")
# for input_path in (Resources.RESOURCES / "samples").glob("*.c"):
#     run(input_path)

# print("INFO: Running others\n")
# for input_path in (Resources.RESOURCES / "others").glob("*.c"):
#     run(input_path)

print("INFO: Running cpp-cheat/c\n")
for input_path in (Resources.RESOURCES / "cpp-cheat" / "c").glob("*.c"):
    # TODO(#2): ..\resources\cpp-cheat\c\complex_h.c
    if input_path.name in ["complex_h.c"]:
        continue
    run(input_path)
# fmt: on
