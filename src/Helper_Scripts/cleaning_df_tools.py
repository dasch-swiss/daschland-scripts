import os
import re

import pandas as pd

pd.set_option("mode.copy_on_write", True)
pd.options.mode.copy_on_write = True


def clean_df_spaces(input_df: pd.DataFrame) -> pd.DataFrame:
    """
    This function strips all the spaces in a df, from column names and the cells, this is relevant when working
    with key excels as spaces in column names do happen, and then we get a key error.
    :param input_df:
    :return:
    """
    # strip the trailing and leading spaces in the column names
    input_df.columns = input_df.columns.str.strip()
    # strip all the spaces in the cells, it has to be of instance str otherwise we get an error
    return input_df.map(lambda x: x.strip() if isinstance(x, str) else x)


def remove_nan_col_rows(df_remove_rows_columns_only_nan: pd.DataFrame) -> pd.DataFrame:
    """
    This function removes all columns and rows, that are completely empty for all values
    :param df_remove_rows_columns_only_nan: the df to work on
    :return:
    """
    df_remove_rows_columns_only_nan.dropna(axis=0, how="all", inplace=True)
    df_remove_rows_columns_only_nan.dropna(axis=1, how="all", inplace=True)
    return df_remove_rows_columns_only_nan


def replace_spaces_with_nan(df_replace_empty_with_nan: pd.DataFrame) -> pd.DataFrame:
    """
    If a cell contains only spaces it will not be recognized as nan even though it is lacks meaning. Therefore,
    we need to replace cells that only contain spaces with nan. It is not advisable to do this with every excel
    as it does take some time. Only if it is relevant if a value is nan or an empty string
    :param df_replace_empty_with_nan: The df that should be cleaned
    :return:
    """
    # this RegEx is true for all columns that are empty (but not nan) or only contains spaces
    # * stands for zero or more of the \s
    empty_re = re.compile(r"^\s*$")

    # we create a function that checks if something is an empty string
    # if it is not of the type string we get a type error
    # we create this function inside the function, as we take the regex as global variable

    def check_string_for_nan(string_value):
        try:
            if empty_re.match(string_value):
                return pd.NA
            else:
                return string_value
        # we get a type error if it not a string, this means either it is a pd.NA or an int, both of which are fine
        except TypeError:
            return string_value

    # we apply the function to the df
    df_replace_empty_with_nan = df_replace_empty_with_nan.map(check_string_for_nan)
    # return the df that is changed
    return df_replace_empty_with_nan


def remove_multiple_spaces_from_df(df_with_spaces: pd.DataFrame) -> pd.DataFrame:
    # compile the regex
    empty_re = re.compile(r"^\s*$")

    def remove_spaces(in_str):
        try:
            li = in_str.split(" ")
            li = [x for x in li if x != ""]
            new_val = " ".join(li)
            if empty_re.match(new_val):
                return pd.NA
            else:
                return new_val
        except TypeError:
            return in_str
        except AttributeError:
            return in_str

    df_with_spaces = df_with_spaces.map(remove_spaces)
    return df_with_spaces


def get_clean_list_images(image_list_unfiltered: list[str]) -> list[str]:
    files_to_archive: dict = {}

    # first iteration for tif
    for image_unfiltered in image_list_unfiltered:
        filename, extension = os.path.splitext(image_unfiltered)
        if extension.lower().endswith(("tif", "tiff")):
            files_to_archive[filename] = extension

    # second iteration for jpg
    for image_unfiltered in image_list_unfiltered:
        filename, extension = os.path.splitext(image_unfiltered)
        if extension.lower().endswith(("jpg", "jpeg")):
            if filename not in files_to_archive.keys():
                files_to_archive[filename] = extension

    # third iteration for jpg
    for image_unfiltered in image_list_unfiltered:
        filename, extension = os.path.splitext(image_unfiltered)
        if extension.lower().endswith("png"):
            if filename not in files_to_archive.keys():
                files_to_archive[filename] = extension

    image_list = [key + files_to_archive[key] for key in files_to_archive]

    return image_list


def create_list(input_value) -> list[str]:
    if pd.isna(input_value):
        return []
    return [x.strip() for x in input_value.split(",")]
