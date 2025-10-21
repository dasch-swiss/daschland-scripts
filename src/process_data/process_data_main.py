from src.folder_paths import (
    ARCHIVE_FOLDER,
    AUDIO_FOLDER,
    BOOK_EDITION_FOLDER,
    DOCUMENTATION_FOLDER,
    INPUT_FOLDER,
    MULTIMEDIA_FOLDER,
    VIDEO_FOLDER,
)
from src.process_data.process_data_helper import (
    update_multimedia_df,
    update_spreadsheet_df,
)


def main() -> None:
    archive_df_name = "Archive"
    multimedia_folder = ARCHIVE_FOLDER
    update_multimedia_df(archive_df_name, multimedia_folder)

    audio_df_name = "Audio"
    multimedia_folder = AUDIO_FOLDER
    update_multimedia_df(audio_df_name, multimedia_folder)

    book_edition_df_name = "BookEdition"
    multimedia_folder = BOOK_EDITION_FOLDER
    update_multimedia_df(book_edition_df_name, multimedia_folder)

    documentation_df_name = "Documentation"
    multimedia_folder = DOCUMENTATION_FOLDER
    update_multimedia_df(documentation_df_name, multimedia_folder)

    image_df_name = "Image"
    update_multimedia_df(image_df_name, MULTIMEDIA_FOLDER, "Multimedia Folder")

    material_df_name = "Material"
    update_multimedia_df(material_df_name, INPUT_FOLDER, "Multimedia Folder")

    video_df_name = "Video"
    multimedia_folder = VIDEO_FOLDER
    update_multimedia_df(video_df_name, multimedia_folder)

    book_df_name = "Book"
    update_spreadsheet_df(book_df_name)

    book_chapter_df_name = "BookChapter"
    update_spreadsheet_df(book_chapter_df_name)

    character_df_name = "Character"
    update_spreadsheet_df(character_df_name)

    event_df_name = "Event"
    update_spreadsheet_df(event_df_name)

    location_df_name = "Location"
    update_spreadsheet_df(location_df_name)

    book_cover_df_name = "BookCover"
    update_spreadsheet_df(book_cover_df_name)

    region_df_name = "Region"
    update_spreadsheet_df(region_df_name)

    video_segment_df_name = "VideoSegment"
    update_spreadsheet_df(video_segment_df_name)

    audio_segment_df_name = "AudioSegment"
    update_spreadsheet_df(audio_segment_df_name)


if __name__ == "__main__":
    main()
