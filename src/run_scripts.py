from dsp_tools import excel2xml
from icecream import ic
from src.Helper_Scripts import helper


# Import scripts
# file names must not contain whitespaces
from src.Scripts import import_archive
from src.Scripts import import_audio
from src.Scripts import import_book
from src.Scripts import import_book_chapter
from src.Scripts import import_character
from src.Scripts import import_documentation
from src.Scripts import import_event
from src.Scripts import import_image
from src.Scripts import import_location
from src.Scripts import import_material
from src.Scripts import import_video

def main():
    root = helper.make_root()

    all_archive = import_archive.main()
    root.extend(all_archive)
    ic(len(all_archive))

    all_audios = import_audio.main()
    root.extend(all_audios)
    ic(len(all_audios))

    all_books = import_book.main()
    root.extend(all_books)
    ic(len(all_books))

    all_book_chapters = import_book_chapter.main()
    root.extend(all_book_chapters)
    ic(len(all_book_chapters))

    all_characters = import_character.main()
    root.extend(all_characters)
    ic(len(all_characters))

    all_documentations = import_documentation.main()
    root.extend(all_documentations)
    ic(len(all_documentations))

    all_events = import_event.main()
    root.extend(all_events)
    ic(len(all_events))

    all_images = import_image.main()
    root.extend(all_images)
    ic(len(all_images))

    all_locations = import_location.main()
    root.extend(all_locations)
    ic(len(all_locations))

    all_materials = import_material.main()
    root.extend(all_materials)
    ic(len(all_materials))

    all_videos = import_video.main()
    root.extend(all_videos)
    ic(len(all_videos))

    excel2xml.write_xml(root, "daschland_data.xml")


if __name__ == "__main__":
    main()
