import pandas as pd

from src.folder_paths import SPREADSHEETS_FOLDER
from src.helpers.image_helper import (
    get_media_file_creation_time,
    get_media_file_size,
)


def update_spreadsheet_df(df_name: str) -> None:
    df = pd.read_excel(SPREADSHEETS_FOLDER / f"{df_name}.xlsx", dtype="str")
    df_cleaned = df.dropna(how="all")
    _write_df_to_csv(df_cleaned, SPREADSHEETS_FOLDER / f"{df_name}.csv")


def update_multimedia_df(df_name: str) -> None:
    df = pd.read_excel(SPREADSHEETS_FOLDER / f"{df_name}.xlsx", dtype="str")
    df_cleaned = df.dropna(how="all")
    df_with_filepath = _add_full_file_path_to_df(df_cleaned)
    updated_df = _add_exif_data_to_df(df_with_filepath)
    _write_df_to_csv(updated_df, SPREADSHEETS_FOLDER / f"{df_name}.csv")


def _add_exif_data_to_df(df: pd.DataFrame) -> pd.DataFrame:
    # Ensure you're working with a copy of the DataFrame
    df_copy = df.copy()
    df_copy.loc[:, "Time Stamp"] = df_copy["File Path"].apply(get_media_file_creation_time)
    df_copy.loc[:, "File Size"] = df_copy["File Path"].apply(get_media_file_size)
    return df_copy


def _add_full_file_path_to_df(df: pd.DataFrame) -> pd.DataFrame:
    df_copy = df.copy()
    df_copy.loc[:, "File Path"] = df_copy.apply(
        lambda row: f"{row['Directory']}{row['File Name']}" if not pd.isna(row["Directory"]) else row["File Name"],
        axis=1,
    )
    return df_copy


def _write_df_to_csv(df: pd.DataFrame, path: str) -> None:
    df.to_csv(path, index=False)
