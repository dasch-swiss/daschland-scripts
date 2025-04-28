from dsp_tools.xmllib import XMLRoot
from icecream import ic


# Import scripts
# file names must not contain whitespaces
from src.Scripts_xmllib import (
    import_archive_new,
    import_audio_new,
    import_audio_segment_new,
    import_book_chapter_new,
    import_book_cover_new,
    import_book_edition_new,
    import_book_new,
    import_character_new,
    import_documentation_new,
    import_event_new,
    import_image_new,
    import_image_region_new,
    import_location_new,
    import_material_new,
    import_video_new,
    import_video_segment_new,
)

from src.Scripts_Nodegoat import Nodegoat_files_update


def main():
    # create the root element dsp-tools
    root = XMLRoot.create_new(shortcode="0854", default_ontology="daschland")

    # import all resources
    all_archive = import_archive_new.main()
    root.add_resource_multiple(all_archive)
    ic(len(all_archive))

    all_audios = import_audio_new.main()
    root = root.add_resource_multiple(all_audios)
    ic(len(all_audios))

    all_audio_segments = import_audio_segment_new.main()
    root = root.add_resource_multiple(all_audio_segments)
    ic(len(all_audio_segments))

    all_books = import_book_new.main()
    root = root.add_resource_multiple(all_books)
    ic(len(all_books))

    all_book_covers = import_book_cover_new.main()
    root = root.add_resource_multiple(all_book_covers)
    ic(len(all_book_covers))

    all_book_editions = import_book_edition_new.main()
    root = root.add_resource_multiple(all_book_editions)
    ic(len(all_book_editions))

    all_book_chapters = import_book_chapter_new.main()
    root = root.add_resource_multiple(all_book_chapters)
    ic(len(all_book_chapters))

    all_characters = import_character_new.main()
    root = root.add_resource_multiple(all_characters)
    ic(len(all_characters))

    all_documentations = import_documentation_new.main()
    root = root.add_resource_multiple(all_documentations)
    ic(len(all_documentations))

    all_events = import_event_new.main()
    root = root.add_resource_multiple(all_events)
    ic(len(all_events))

    all_images = import_image_new.main()
    root = root.add_resource_multiple(all_images)
    ic(len(all_images))

    all_regions = import_image_region_new.main()
    root = root.add_resource_multiple(all_regions)
    ic(len(all_regions))

    all_locations = import_location_new.main()
    root = root.add_resource_multiple(all_locations)
    ic(len(all_locations))

    all_materials = import_material_new.main()
    root = root.add_resource_multiple(all_materials)
    ic(len(all_materials))

    all_videos = import_video_new.main()
    root = root.add_resource_multiple(all_videos)
    ic(len(all_videos))

    all_video_segments = import_video_segment_new.main()
    root = root.add_resource_multiple(all_video_segments)
    ic(len(all_video_segments))

    # write the root to a xml file
    root.write_file("daschland_data.xml")

    # update nodegoat files
    Nodegoat_files_update.main()
    ic("Nodegoat files updated")


if __name__ == "__main__":
    main()
