import pathlib
from pathlib import Path
from typing import Optional

import pandas as pd

from src.folder_paths import PROCESSED_FOLDER, RAW_FOLDER
from src.helpers.image_helper import (
    get_media_file_creation_time,
    get_media_file_size,
)


def update_spreadsheet_df(class_name: str) -> None:
    df = pd.read_excel(RAW_FOLDER / f"{class_name}.xlsx", dtype="str")
    df_cleaned = df.dropna(how="all")
    _write_df_to_csv(df_cleaned, PROCESSED_FOLDER / f"{class_name}.csv")


def update_multimedia_df(
    class_name: str, multimedia_folder: pathlib.Path, alternative_column: Optional[str] = None
) -> None:
    df = pd.read_excel(RAW_FOLDER / f"{class_name}.xlsx", dtype="str")
    df_cleaned = df.dropna(how="all")
    if alternative_column is None:
        updated_df = _add_absolute_file_paths(df_cleaned, multimedia_folder)
    else:
        updated_df = _add_absolute_file_paths_with_multiple_folders(df_cleaned, multimedia_folder)
    updated_df = _add_exif_data_to_df(updated_df)
    # remove the temporary column as we do not want to save absolute paths in the file
    updated_df.pop("AbsoluteFilePath")
    _write_df_to_csv(df=updated_df, path=PROCESSED_FOLDER / f"{class_name}.csv")


def _add_absolute_file_paths(df: pd.DataFrame, multimedia_folder: pathlib.Path) -> pd.DataFrame:
    # Ensure you're working with a copy of the DataFrame
    df_copy = df.copy()
    # Construct a Series of Path objects
    df_copy["AbsoluteFilePath"] = df_copy["File Name"].apply(
        lambda x: str(multimedia_folder / x)
    )  # Now apply your functions to the Series
    return df_copy


def _add_absolute_file_paths_with_multiple_folders(
    df: pd.DataFrame, generic_multimedia_folder: pathlib.Path
) -> pd.DataFrame:
    df_copy = df.copy()
    df_copy["Multimedia Folder"] = df_copy["Multimedia Folder"].apply(lambda x: generic_multimedia_folder / x)
    for i, row in df_copy.iterrows():
        df_copy.loc[i, "AbsoluteFilePath"] = row["Multimedia Folder"] / row["File Name"]  # type: ignore[index]
    return df_copy


def _add_exif_data_to_df(df: pd.DataFrame) -> pd.DataFrame:
    df_copy = df.copy()
    df_copy["Time Stamp"] = df_copy["AbsoluteFilePath"].apply(get_media_file_creation_time)
    df_copy["File Size"] = df_copy["AbsoluteFilePath"].apply(get_media_file_size)
    return df_copy


def _write_df_to_csv(df: pd.DataFrame, path: Path) -> None:
    df.to_csv(path, index=False)
