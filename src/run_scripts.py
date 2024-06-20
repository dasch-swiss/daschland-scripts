from dsp_tools import excel2xml
from icecream import ic
from src.Helper_Scripts import helper


# Import scripts
# file names must not contain whitespaces
from src.Scripts import import_animal_character
from src.Scripts import import_audio
from src.Scripts import import_character
from src.Scripts import import_archive
from src.Scripts import import_book
from src.Scripts import import_book_chapter
from src.Scripts import import_documentation
from src.Scripts import import_image_human
from src.Scripts import import_image
from src.Scripts import import_image_wonderland_character
from src.Scripts import import_location
from src.Scripts import import_material
from src.Scripts import import_video
from src.Scripts import import_character

def main():
    root = helper.make_root()

    all_animal_characters = import_animal_character.main()
    root.extend(all_animal_characters)
    ic(len(all_animal_characters))

    all_audios = import_audio.main()
    root.extend(all_audios)
    ic(len(all_audios))

    all_characters = import_character.main()
    root.extend(all_characters)
    ic(len(all_characters))

    all_dungeons = import_dungeon.main()
    root.extend(all_dungeons)
    ic(len(all_dungeons))

    all_fairytales = import_fairytale.main()
    root.extend(all_fairytales)
    ic(len(all_fairytales))

    all_fairytale_chapters = import_fairytale_chapter.main()
    root.extend(all_fairytale_chapters)
    ic(len(all_fairytale_chapters))

    all_flyers = import_flyer.main()
    root.extend(all_flyers)
    ic(len(all_flyers))

    all_images_human = import_image_human.main()
    root.extend(all_images_human)
    ic(len(all_images_human))

    all_images_animal = import_image_animal.main()
    root.extend(all_images_animal)
    ic(len(all_images_animal))

    all_images_wonderland_character = import_image_wonderland_character.main()
    root.extend(all_images_wonderland_character)
    ic(len(all_images_wonderland_character))

    all_locations = import_location.main()
    root.extend(all_locations)
    ic(len(all_locations))

    all_originals = import_originals.main()
    root.extend(all_originals)
    ic(len(all_originals))

    all_videos = import_video.main()
    root.extend(all_videos)
    ic(len(all_videos))

    all_wonderland_characters = import_wonderland_character.main()
    root.extend(all_wonderland_characters)
    ic(len(all_wonderland_characters))


    excel2xml.write_xml(root, "daschland_data.xml")


if __name__ == "__main__":
    main()
