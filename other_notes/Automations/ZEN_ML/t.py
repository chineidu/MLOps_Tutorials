# from typing import Any

# import pandas as pd
# import polars as pl
# from typeguard import typechecked

# df: pl.DataFrame = pl.DataFrame(data={"name": ["a", "b", "c"], "age": [1, 2, 3]})

# print(df.shape)


# @typechecked
# def _get_datatrame_metadata(data: pl.DataFrame | pd.DataFrame) -> dict[str, Any]:
#     return {
#         "shape": {"n_rows": data.shape[0], "n_columns": data.shape[1]},
#         "columns": data.columns,
#         "summary_stats": data.describe().to_dicts(),
#     }


# print(_get_datatrame_metadata(df))
