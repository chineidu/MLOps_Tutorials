# Jupyter Notebook

- Boilerplate code

## Table of Content

- [Jupyter Notebook](#jupyter-notebook)
  - [Table of Content](#table-of-content)
  - [Check Installed Dependencies](#check-installed-dependencies)
    - [Approach 1](#approach-1)
    - [Approach 2](#approach-2)
  - [Boilerplate 1](#boilerplate-1)
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
        "info": "#76FF7B",
        "warning": "#FBDDFE",
        "error": "#FF0000",
    }
)
console = Console(theme=custom_theme)

# Visualization
import matplotlib.pyplot as plt


# Pandas settings
pd.options.display.max_rows = 1_000
pd.options.display.max_columns = 1_000
pd.options.display.max_colwidth = 600

warnings.filterwarnings("ignore")

# Add seed
np.random.seed(0)

# Black code formatter (Optional)
%load_ext lab_black

# auto reload imports
%load_ext autoreload
%autoreload 2
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
