from pathlib import Path


class Resources:
    ROOT = Path(__file__).parent

    RESOURCES = ROOT / "resources"
    SAMPLES = RESOURCES / "samples"

    BUILD = ROOT / "build"
    OUTPUTS = BUILD / "outputs"

    VENDOR = ROOT / "vendor"

    @staticmethod
    def get_sample(name: str):
        return Resources.SAMPLES / name

    @staticmethod
    def get_output(name: str):
        return Resources.OUTPUTS / name


dirs = [
    Resources.OUTPUTS,
    Resources.BUILD,
    Resources.VENDOR
]

for it in dirs:
    it.mkdir(parents=True, exist_ok=True)
