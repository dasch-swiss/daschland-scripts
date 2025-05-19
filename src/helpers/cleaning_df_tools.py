from typing import Any

import pandas as pd


def create_list(input_value: Any) -> list[str]:
    if pd.isna(input_value):
        return []
    return [x.strip() for x in input_value.split(",")]
