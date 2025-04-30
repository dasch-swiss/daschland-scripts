import os
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from exiftool import ExifToolHelper
from PIL import Image
from PIL.ExifTags import TAGS


def get_image_creation_time(image_path: str) -> Optional[str]:
    image_path = os.path.expanduser(image_path)
    # convert image_path into pathlib object:
    image_path_conform = Path(image_path)

    # Open the image file
    image = Image.open(image_path_conform)

    # Extract EXIF data
    exif_data: dict[str, Any] = image._getexif()  # type: ignore[attr-defined]
    # If no EXIF data found
    if not exif_data:
        return None

    date_time_raw = _get_time_from_exif_data(exif_data)
    if not date_time_raw:
        return None

    # convert the creation time to CE time
    time_conform = _convert_creation_time_to_dsp_time(date_time_raw)
    if time_conform:
        return time_conform
    else:
        return None


def _get_time_from_exif_data(exif_data: dict[str, str]) -> str | None:
    # Loop through the EXIF data to find the creation time
    for tag, value in exif_data.items():
        tag_name = TAGS.get(tag, tag)
        if tag_name == "DateTimeOriginal":
            return value
        else:
            continue
    return None


def _convert_creation_time_to_dsp_time(time: str):
    input_format = "%Y:%m:%d %H:%M:%S"
    output_format = "%Y-%m-%dT%H:%M:%S-00:00"
    try:
        time_to_convert = datetime.strptime(time, input_format)
        return time_to_convert.strftime(output_format)
    except ValueError:
        return None


def get_media_file_creation_time(file_path: str) -> Optional[str]:
    try:
        with ExifToolHelper() as et:
            metadata_list = et.get_metadata(file_path)
            if not metadata_list:
                return None

            metadata = metadata_list[0]
            # Loop through metadata to find the first valid CreateDate
            for key, value in metadata.items():
                if key.endswith("CreateDate"):
                    return _convert_media_creation_time_to_dsp_time(value)
            return None
    except Exception as e:  # noqa: BLE001 (Do not catch blind exceptions)
        print(f"Error processing file {file_path}: {e}")
        return None


def _convert_media_creation_time_to_dsp_time(time: str) -> str | None:
    # Define the input date format

    # Parse the date string into a datetime object
    date_formats = ["%Y:%m:%d %H:%M:%SZ", "%Y:%m:%dT%H:%M:%Sz", "%Y:%m:%d %H:%M:%S"]
    output_format = "%Y-%m-%dT%H:%M:%S-00:00"

    for date_format in date_formats:
        try:
            time_to_convert = datetime.strptime(time, date_format)
            return time_to_convert.strftime(output_format)
        except ValueError:
            continue
    return None


def get_media_file_size(file_path: str) -> Optional[str]:
    with ExifToolHelper() as et:
        metadata_list = et.get_metadata(file_path)
        if metadata_list:
            metadata = metadata_list[0]
            file_size = None
            for key, value in metadata.items():
                if key.endswith("Size"):
                    file_size = value
                    break
        else:
            return None

    if file_size:
        size_mb = _convert_bytes_to_mb(file_size)
        return round(size_mb, 3)
    else:
        return None


def _convert_bytes_to_mb(bytes_size):
    # 1 MB = 1024 * 1024 bytes
    megabytes_size = bytes_size / (1024 * 1024)
    return megabytes_size
