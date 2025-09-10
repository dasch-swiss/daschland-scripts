import pandas as pd
from dsp_tools.xmllib import (
    LicenseRecommended,
    Permissions,
    Resource,
    create_list_from_input,
)

from src.helpers.image_helper import get_image_creation_time, get_media_file_size


def main() -> list[Resource]:
    all_resources: list[Resource] = []

    # define dataframe
    image_df = pd.read_excel("data/spreadsheets/Image.xlsx", dtype="str")

    # iterate through rows of dataframe:
    for _, row in image_df.iterrows():
        # define variables
        image_path = f"{row['Directory']}{row['File Name']}"
        timestamp_value = get_image_creation_time(image_path)
        file_size_value = get_media_file_size(image_path)
        chapter_id = create_list_from_input(row["Chapter ID"], separator=",")
        character_id = create_list_from_input(row["Character ID"], separator=",")
        file_permissions = (
            Permissions.LIMITED_VIEW if row["Limited View"] == "yes" else Permissions.PROJECT_SPECIFIC_PERMISSIONS
        )
        authors = create_list_from_input(input_value=row["Authorship"], separator=",")
        authors_resource = create_list_from_input(input_value=row["Authorship Resource"], separator=",")

        if row["Limited View"] == "yes":
            restype = ":ImageAlternative"
            description = row["Description Alternative"]
            description_property = ":hasDescriptionAlternative"
        else:
            restype = ":ImageOriginal"
            description = row["Description"]
            description_property = ":hasDescription"

        # create resource, label and id
        resource = Resource.create_new(res_id=row["ID"], restype=restype, label=description)

        # add file to resource
        resource.add_file(
            filename=image_path,
            permissions=file_permissions,
            license=LicenseRecommended.DSP.PUBLIC_DOMAIN,
            copyright_holder=row["Copyright"],
            authorship=authors,
        )

        # add properties to resource
        resource.add_simpletext(value=row["ID"], prop_name="project-metadata:hasID")
        resource.add_time_optional(value=timestamp_value, prop_name="project-metadata:hasTimeStamp")
        resource.add_decimal_optional(value=file_size_value, prop_name="project-metadata:hasFileSize")
        resource.add_simpletext("project-metadata:hasCopyrightResource", "DaSCH")
        resource.add_list("project-metadata:hasLicenseResource", "License", "LIC_002")
        resource.add_simpletext_multiple("project-metadata:hasAuthorshipResource", authors_resource)
        resource.add_simpletext(":hasFileName", row["File Name"])
        resource.add_link_multiple(":isPartOfBookChapter", chapter_id)
        resource.add_link_multiple(":isPartOfCharacter", character_id)
        resource.add_integer(":hasSeqnum", row["Seqnum"])
        resource.add_richtext_optional(prop_name=description_property, value=description)
        # append resource to list
        all_resources.append(resource)

    return all_resources


if __name__ == "__main__":
    main()
