from pathlib import Path
from typing import Optional

from c_inspectors.resources import Resources

from c_inspectors.parse_and_transform_file import ParserAndTransformFile


def process_sample(sample_name: str, input_path: Optional[Path] = None):
    ParserAndTransformFile(
        input_path=input_path or Resources.get_sample(sample_name),
        output_path=Resources.get_output(sample_name),
        json_path=Resources.get_output(sample_name.replace('.c', '.json'))
    ).enable_log().run()
    print()


# fmt: off
process_sample("empty.c")
process_sample("only-fork-1.c")
process_sample("only-fork-2.c")
process_sample("only-fork-3.c")
process_sample("program1.2.c")
process_sample("program1.3.c")
process_sample("program1.4.c")
process_sample("program1.5.c")
process_sample("program1.6.c")
process_sample("program1.7.c")
process_sample("program1.8.c")
process_sample("program1.9.c")
process_sample("program1.10.c")
process_sample("program1.11.1.c")
process_sample("program1.11.2.c")
process_sample("program1.12.1.c")
process_sample("program1.12.2.c")
process_sample("program1.13.1.c")
process_sample("program1.13.2.c")
process_sample("program1.13.3.c")
process_sample("program1.14.c")
process_sample("for.c", (Resources.RESOURCES / "others" / "for.c"))
process_sample("enter_exit.c", (Resources.RESOURCES / "others" / "enter_exit.c"))
process_sample("features.c", (Resources.RESOURCES / "others" / "features.c"))
process_sample("inspectors.c", (Resources.RESOURCES / "others" / "inspectors.c"))
# fmt: on
