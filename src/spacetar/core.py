from pathlib import Path
from importlib.metadata import version, PackageNotFoundError

__here__ = Path(__file__).parent.resolve()

try:
    __version__ = version("spacetar")
except PackageNotFoundError:
    pass
