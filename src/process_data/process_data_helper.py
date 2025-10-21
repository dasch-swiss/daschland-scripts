from pathlib import Path

import pandas as pd

from src.folder_paths import PROCESSED_FOLDER, RAW_FOLDER
from src.helpers.image_helper import (
    get_media_file_creation_time,
    get_media_file_size,
)


def update_spreadsheet_df(df_name: str) -> None:
    df = pd.read_excel(RAW_FOLDER / f"{df_name}.xlsx", dtype="str")
    df_cleaned = df.dropna(how="all")
    _write_df_to_csv(df_cleaned, PROCESSED_FOLDER / f"{df_name}.csv")


def update_multimedia_df(df_name: str, default_multimedia_folder, alternative_column=None) -> None:
    df = pd.read_excel(RAW_FOLDER / f"{df_name}.xlsx", dtype="str")
    df_cleaned = df.dropna(how="all")
    multimedia_folder = (default_multimedia_folder/df[alternative_column] if alternative_column is not None else default_multimedia_folder)
    updated_df = _add_exif_data_to_df(df_cleaned, multimedia_folder)
    _write_df_to_csv(df=updated_df, path=PROCESSED_FOLDER / f"{df_name}.csv")


def _add_exif_data_to_df(df: pd.DataFrame, multimedia_folder) -> pd.DataFrame:
    # Ensure you're working with a copy of the DataFrame
    df_copy = df.copy()
    filepath = multimedia_folder/df_copy["File Name"]
    df_copy.loc[:, "Time Stamp"] = filepath.apply(get_media_file_creation_time)
    df_copy.loc[:, "File Size"] = filepath.apply(get_media_file_size)
    return df_copy


def _write_df_to_csv(df: pd.DataFrame, path: Path) -> None:
    df.to_csv(path, index=False)
