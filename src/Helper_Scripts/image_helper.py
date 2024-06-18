from PIL import Image
from PIL.ExifTags import TAGS
from pathlib import Path
import os
from datetime import datetime
import exiftool

def get_image_creation_time(image_path) -> str:
    image_path = os.path.expanduser(image_path)
    #convert image_path into pathlib object:
    image_path_conform = Path(image_path)

    # Open the image file
    image = Image.open(image_path_conform)

    # Extract EXIF data
    exif_data = image._getexif()
    # If no EXIF data found
    if not exif_data:
        return None

    date_time_raw = _get_Time_from_exif_data(exif_data)
    if not date_time_raw:
        return None

    # convert the creation time to CE time
    time_conform = _convert_creation_time_to_DSP_time(date_time_raw)
    if time_conform:
        return time_conform
    else:
        return None

def _get_Time_from_exif_data(exif_data):
    # Loop through the EXIF data to find the creation time
    for tag, value in exif_data.items():
        tag_name = TAGS.get(tag, tag)
        if tag_name == 'DateTimeOriginal':
            return value
        else:
            continue

def _convert_creation_time_to_DSP_time(time):
    input_format = '%Y:%m:%d %H:%M:%S'
    output_format = '%Y-%m-%dT%H:%M:%S-00:00'
    try:
        time_to_convert = datetime.strptime(time, input_format)
        return time_to_convert.strftime(output_format)
    except ValueError:
        return None


def get_media_file_creation_time(file_path: str) -> str:
    with exiftool.ExifToolHelper() as et:
        metadata_list = et.get_metadata(file_path)
        if metadata_list:
            metadata = metadata_list[0]
            creation_time = metadata.get('QuickTime:CreateDate')
    if creation_time: # Convert the creation time to the desired format
        creation_time_conform = _convert_media_creation_time_to_DSP_time(creation_time)
        return creation_time_conform
    else:
        return None

def _convert_media_creation_time_to_DSP_time(time: str) -> str:
    # Define the input date format
    input_format = "%Y:%m:%d %H:%M:%S"

    # Parse the date string into a datetime object
    try:
        time_to_convert = datetime.strptime(time, input_format)
    except ValueError:
        input_format = "%Y-%m-%dT%H:%M:%S%z"
        time_to_convert = datetime.strptime(time, input_format)

    # Format the datetime object into the desired output format
    output_format = "%Y-%m-%dT%H:%M:%S-00:00"
    transformed_date_str = time_to_convert.strftime(output_format)

    return transformed_date_str