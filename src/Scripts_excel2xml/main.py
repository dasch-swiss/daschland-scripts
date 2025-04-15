from dsp_tools import excel2xml
from icecream import ic
from src.Helper_Scripts import helper


# Import scripts
# file names must not contain whitespaces
from src.Scripts_excel2xml import (
    import_documentation,
    import_book_edition,
    import_image_region,
    import_location,
    import_audio_segment,
    import_book,
    import_archive,
    import_image,
    import_book_cover,
    import_character,
    import_event,
    import_book_chapter,
    import_material,
    import_audio,
    import_video_segment,
    import_video,
)

from src.Scripts_Nodegoat import Nodegoat_files_update


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

    all_book_covers = import_book_cover.main()
    root.extend(all_book_covers)
    ic(len(all_book_covers))

    all_book_editions = import_book_edition.main()
    root.extend(all_book_editions)
    ic(len(all_book_editions))

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

    all_regions = import_image_region.main()
    root.extend(all_regions)
    ic(len(all_regions))

    all_video_segments = import_video_segment.main()
    root.extend(all_video_segments)
    ic(len(all_video_segments))

    all_audio_segments = import_audio_segment.main()
    root.extend(all_audio_segments)
    ic(len(all_audio_segments))

    excel2xml.write_xml(root, "daschland_data_excel2xml.xml")

    Nodegoat_files_update.main()


if __name__ == "__main__":
    main()
