from pathlib import Path


class Resources:
    ROOT = Path(__file__).parent

    RESOURCES = ROOT / ".." / "resources"

    BUILD = ROOT / "build"
    OUTPUTS = RESOURCES / "outputs"

    VENDOR = ROOT / "vendor"


dirs = [
    Resources.OUTPUTS,
    Resources.BUILD,
    Resources.VENDOR
]

for it in dirs:
    it.mkdir(parents=True, exist_ok=True)
