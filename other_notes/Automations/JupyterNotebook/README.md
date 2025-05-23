# Jupyter Notebook

- Boilerplate code

## Table of Content

- [Jupyter Notebook](#jupyter-notebook)
  - [Table of Content](#table-of-content)
  - [Check Installed Dependencies](#check-installed-dependencies)
    - [Approach 1](#approach-1)
    - [Approach 2](#approach-2)
  - [Boilerplate 1](#boilerplate-1)
  - [Rich Customisations](#rich-customisations)
  - [Custom Functions](#custom-functions)
  - [Run Ollama](#run-ollama)
  - [Jupyter Notebook Strip Output](#jupyter-notebook-strip-output)

## Check Installed Dependencies

- Required:

```sh
pip install watermark
```

### Approach 1

```py
%load_ext watermark
%watermark -v -p numpy,pandas,polars,torch,lightning --conda

# ==== Output ====
# Python implementation: CPython
# Python version       : 3.10.8
# IPython version      : 8.23.0

# numpy    : 1.26.4
# pandas   : 2.2.2
# polars   : 0.20.21
# torch    : 2.2.2
# lightning: 2.2.2

# conda environment: n/a
```

### Approach 2

```py
from watermark import watermark

print(watermark(packages="polars,scikit-learn,torch,lightning", python=True))

# ==== Output ====
# Python implementation: CPython
# Python version       : 3.10.8
# IPython version      : 8.23.0

# polars      : 0.20.21
# scikit-learn: 1.4.2
# torch       : 2.2.2
# lightning   : 2.2.2
```

## Boilerplate 1

```py
# Built-in library
from pathlib import Path
import re
import json
from typing import Any, Optional, Union
import logging
import warnings

# Standard imports
import numpy as np
import numpy.typing as npt
from pprint import pprint
import pandas as pd
import polars as pl
from rich.console import Console
from rich.theme import Theme

custom_theme = Theme(
    {
        "white": "#FFFFFF",  # Bright white
        "info": "#00FF00",  # Bright green
        "warning": "#FFD700",  # Bright gold
        "error": "#FF1493",  # Deep pink
        "success": "#00FFFF",  # Cyan
        "highlight": "#FF4500",  # Orange-red
    }
)
console = Console(theme=custom_theme)

# Visualization
import matplotlib.pyplot as plt

# NumPy settings
np.set_printoptions(precision=4)

# Pandas settings
pd.options.display.max_rows = 1_000
pd.options.display.max_columns = 1_000
pd.options.display.max_colwidth = 600

# Polars settings
pl.Config.set_fmt_str_lengths(1_000)
pl.Config.set_tbl_cols(n=1_000)

warnings.filterwarnings("ignore")

# Black code formatter (Optional)
%load_ext lab_black

# auto reload imports
%load_ext autoreload
%autoreload 2
```

## Rich Customisations

```py
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich import box
from rich.theme import Theme

custom_theme = Theme(
    {
        "white": "#FFFFFF",  # Bright white
        "info": "#00FF00",  # Bright green
        "warning": "#FFD700",  # Bright gold
        "error": "#FF1493",  # Deep pink
        "success": "#00FFFF",  # Cyan
        "highlight": "#FF4500",  # Orange-red
    }
)

console = Console(theme=custom_theme)


def fancy_print(
    object: Any,
    title: str = "Result",
    border_style: str = "bright_green",
    content_style: str | None = None,
    show_type: bool = True,
    expand: bool = False,
    return_panel: bool = False,
) -> Panel | None:

    if isinstance(object, dict):
        content = Table(show_header=False, box=box.SIMPLE)
        for key, value in object.items():
            content.add_row(
                Text(str(key), style="cyan"),
                Text(str(value), style=content_style or "white"),
            )
    elif isinstance(object, (list, tuple)):
        content = Table(show_header=False, box=box.SIMPLE)
        for i, item in enumerate(object):
            content.add_row(
                Text(str(i), style="cyan"),
                Text(str(item), style=content_style or "white"),
            )
    else:
        content = Text(str(object), style=content_style or "white")

    if show_type:
        title = f"{title} ({type(object).__name__})"

    panel = Panel(
        content,
        title=title,
        title_align="left",
        border_style=border_style,
        expand=expand,
    )
    if return_panel:
        return panel
    else:
        console.print(panel)
        return None


# Example usage
console.print("hello, world!")
fancy_print({"message": "Good morning!", "name": "John"})
```

## Custom Functions

```py

def go_up_from_current_directory(*, go_up: int = 1) -> None:
    """This is used to up a number of directories.

    Params:
    -------
    go_up: int, default=1
        This indicates the number of times to go back up from the current directory.

    Returns:
    --------
    None
    """
    import os
    import sys

    CONST: str = "../"
    NUM: str = CONST * go_up

    # Goto the previous directory
    prev_directory = os.path.join(os.path.dirname(__name__), NUM)
    # Get the 'absolute path' of the previous directory
    abs_path_prev_directory = os.path.abspath(prev_directory)

    # Add the path to the System paths
    sys.path.insert(0, abs_path_prev_directory)
    print(abs_path_prev_directory)
```

## Run Ollama

```sh
export OLLAMA_FLASH_ATTENTION=1 OLLAMA_KEEP_ALIVE="15m" \
    OLLAMA_NUM_THREADS=8 OLLAMA_MAX_LOADED=2 OLLAMA_NUM_PARALLEL=2 \
    && ollama serve > logs.txt 2>&1
```

## [Jupyter Notebook Strip Output](https://github.com/kynan/nbstripout)

```sh
# installation
pip install --upgrade nbstripout

# Configure filter
git config --global filter.nbstripout.clean 'nbstripout'

# Remove empty cells
nbstripout --drop-empty-cells
```
