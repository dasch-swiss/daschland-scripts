from PIL import Image
from PIL.ExifTags import TAGS

def get_image_creation_time(image_path) -> str:
    # Open the image file
    image = Image.open(image_path)

    # Extract EXIF data
    exif_data = image._getexif()

    # If no EXIF data found
    if not exif_data:
        return None

    # Loop through the EXIF data to find the creation time
    for tag, value in exif_data.items():
        tag_name = TAGS.get(tag, tag)
        if tag_name == 'DateTimeOriginal':
            return value

    return None