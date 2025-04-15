import pandas as pd


def make_cols_mapping_with_columns(
    df: pd.DataFrame, value_column, key_column="ID"
) -> dict[str, str]:
    """
    This method takes a pandas DataFrame where one must select two columns,
    and creates a mapping from the values in the first column to the values in the second column.
    The resulting dictionary has the same length as the two columns.
    """
    new_df = df.dropna(axis="index", subset=value_column)

    return dict(zip(new_df[key_column], new_df[value_column]))
