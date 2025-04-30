from dsp_tools.xmllib import XMLRoot
from icecream import ic


# Import scripts
# file names must not contain whitespaces
from src.Scripts_xmllib import (
    import_archive,
    import_audio,
    import_audio_segment,
    import_book_chapter,
    import_book_cover,
    import_book_edition,
    import_book,
    import_character,
    import_documentation,
    import_event,
    import_image,
    import_image_region,
    import_location,
    import_material,
    import_video,
    import_video_segment,
)

from src.Scripts_Nodegoat import Nodegoat_files_update


def main() -> None:
    # create the root element dsp-tools
    root = XMLRoot.create_new(shortcode="0854", default_ontology="daschland")

    # import all resources
    all_archive = import_archive.main()
    root.add_resource_multiple(all_archive)
    ic(len(all_archive))

    all_audios = import_audio.main()
    root = root.add_resource_multiple(all_audios)
    ic(len(all_audios))

    all_audio_segments = import_audio_segment.main()
    root = root.add_resource_multiple(all_audio_segments)
    ic(len(all_audio_segments))

    all_books = import_book.main()
    root = root.add_resource_multiple(all_books)
    ic(len(all_books))

    all_book_covers = import_book_cover.main()
    root = root.add_resource_multiple(all_book_covers)
    ic(len(all_book_covers))

    all_book_editions = import_book_edition.main()
    root = root.add_resource_multiple(all_book_editions)
    ic(len(all_book_editions))

    all_book_chapters = import_book_chapter.main()
    root = root.add_resource_multiple(all_book_chapters)
    ic(len(all_book_chapters))

    all_characters = import_character.main()
    root = root.add_resource_multiple(all_characters)
    ic(len(all_characters))

    all_documentations = import_documentation.main()
    root = root.add_resource_multiple(all_documentations)
    ic(len(all_documentations))

    all_events = import_event.main()
    root = root.add_resource_multiple(all_events)
    ic(len(all_events))

    all_images = import_image.main()
    root = root.add_resource_multiple(all_images)
    ic(len(all_images))

    all_regions = import_image_region.main()
    root = root.add_resource_multiple(all_regions)
    ic(len(all_regions))

    all_locations = import_location.main()
    root = root.add_resource_multiple(all_locations)
    ic(len(all_locations))

    all_materials = import_material.main()
    root = root.add_resource_multiple(all_materials)
    ic(len(all_materials))

    all_videos = import_video.main()
    root = root.add_resource_multiple(all_videos)
    ic(len(all_videos))

    all_video_segments = import_video_segment.main()
    root = root.add_resource_multiple(all_video_segments)
    ic(len(all_video_segments))

    # write the root to a xml file
    root.write_file("daschland_data.xml")

    # update nodegoat files
    Nodegoat_files_update.main()
    ic("nodegoat files updated")


if __name__ == "__main__":
    main()
