"""This is used to manage configuration files."""
from pathlib import Path

# Custom Imports
import src

SRC_ROOT = Path(src.__file__).absolute().parent  # src/
ROOT = SRC_ROOT.parent  # proj/src
DATA_FILEPATH = ROOT / "data"
