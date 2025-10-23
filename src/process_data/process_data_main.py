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
    update_multimedia_df("Archive", ARCHIVE_FOLDER)

    update_multimedia_df("Audio", AUDIO_FOLDER)

    update_multimedia_df("BookEdition", BOOK_EDITION_FOLDER)

    update_multimedia_df("Documentation", DOCUMENTATION_FOLDER)

    update_multimedia_df("Image", MULTIMEDIA_FOLDER, "Multimedia Folder")

    update_multimedia_df("Material", INPUT_FOLDER, "Multimedia Folder")

    update_multimedia_df("Video", VIDEO_FOLDER)

    update_spreadsheet_df("Book")

    update_spreadsheet_df("BookChapter")

    update_spreadsheet_df("Character")

    update_spreadsheet_df("Event")

    update_spreadsheet_df("Location")

    update_spreadsheet_df("BookCover")

    update_spreadsheet_df("Region")

    update_spreadsheet_df("VideoSegment")

    update_spreadsheet_df("AudioSegment")

    update_spreadsheet_df("LinkObject")


if __name__ == "__main__":
    main()
