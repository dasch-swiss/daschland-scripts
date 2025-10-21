import pandas as pd
from dsp_tools.xmllib import Resource, create_list_from_input, find_license_in_string

from src.folder_paths import AUDIO_FOLDER, RAW_FOLDER
from src.helpers.image_helper import (
    get_media_file_creation_time,
    get_media_file_size,
)


def main() -> list[Resource]:
    all_resources: list[Resource] = []

    # define dataframe
    audio_df = pd.read_excel(RAW_FOLDER / "Audio.xlsx", dtype="str")

    # iterate through rows of dataframe:
    for _, row in audio_df.iterrows():
        # define variables
        audio_path = f"{AUDIO_FOLDER/row['File Name']}"
        timestamp_value = get_media_file_creation_time(audio_path)
        file_size_value = get_media_file_size(audio_path)
        authors = create_list_from_input(row["Authorship"], separator=", ")
        authors_resource = create_list_from_input(row["Authorship Resource"], separator=", ")
        file_license = find_license_in_string(row["License List"])
        # create resource, label and id
        resource = Resource.create_new(res_id=row["ID"], restype=":Audio", label=row["Name"])

        # add file to resource
        resource.add_file(
            filename=audio_path,
            license=file_license,
            copyright_holder=row["Copyright"],
            authorship=authors,
        )

        # add properties to resource
        resource.add_simpletext("project-metadata:hasID", row["ID"])
        resource.add_time_optional("project-metadata:hasTimeStamp", timestamp_value)
        resource.add_decimal_optional("project-metadata:hasFileSize", file_size_value)
        resource.add_simpletext("project-metadata:hasFileName", row["File Name"])
        resource.add_richtext(":hasDescription", row["Description"])
        resource.add_textarea_optional(":hasCast", row["Cast"])
        resource.add_simpletext("project-metadata:hasCopyrightResource", "DaSCH")
        resource.add_list("project-metadata:hasLicenseResource", "License", "LIC_002")
        resource.add_simpletext_multiple("project-metadata:hasAuthorshipResource", authors_resource)

        # append resource to list
        all_resources.append(resource)

    return all_resources


if __name__ == "__main__":
    main()
