from json import loads
from pathlib import Path
from importlib.metadata import version, PackageNotFoundError

whoami = "spacetar"
whereami = Path(__file__).parent.resolve()
freezer = whereami / "data" / f"{whoami}.db"
waves = ["submm", "mm", "cm", "IR", "Vis", "UV"]
data = lambda _: loads((whereami / "data" / f"{_}.json").read_text())

try:
    __version__ = version(whoami)
except PackageNotFoundError:
    pass
