import pandas as pd
from dsp_tools.xmllib import LicenseRecommended, Resource, create_list_from_input, is_nonempty_value

from src.helpers.image_helper import (
    get_media_file_creation_time,
    get_media_file_size,
)


def main() -> list[Resource]:
    all_resources: list[Resource] = []

    # define dataframe
    material_df = pd.read_excel("data/spreadsheets/Material.xlsx", dtype="str")

    # iterate through rows of dataframe:
    for _, row in material_df.iterrows():
        originals_path = (
            f"{row['Directory']}{row['File Name']}" if is_nonempty_value(row["Directory"]) else row["File Name"]
        )
        timestamp_value = get_media_file_creation_time(originals_path)
        file_size_value = get_media_file_size(originals_path)
        authors = create_list_from_input(input_value=row["Authorship"], separator=",")
        authors_resource = create_list_from_input(input_value=row["Authorship Resource"], separator=",")

        # create resource, label and id
        resource = Resource.create_new(res_id=row["ID"], restype="project-metadata:Material", label=row["File Name"])

        # add file to resource
        resource.add_file(
            originals_path, license=LicenseRecommended.CC.BY, copyright_holder=row["Copyright"], authorship=authors
        )

        # add properties to resource
        resource.add_simpletext("project-metadata:hasID", row["ID"])
        resource.add_simpletext("project-metadata:hasFileName", row["File Name"])
        resource.add_richtext("project-metadata:hasFileDescription", row["Description"])
        resource.add_time_optional("project-metadata:hasTimeStamp", timestamp_value)
        resource.add_decimal_optional("project-metadata:hasFileSize", file_size_value)
        resource.add_simpletext("project-metadata:hasCopyrightResource", "DaSCH")
        resource.add_list("project-metadata:hasLicenseResource", "License", "LIC_002")
        resource.add_simpletext_multiple("project-metadata:hasAuthorshipResource", authors_resource)
        # append resource to list
        all_resources.append(resource)

    return all_resources


if __name__ == "__main__":
    main()
