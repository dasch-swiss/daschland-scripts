import pandas as pd
from dsp_tools.xmllib import (
    LicenseRecommended,
    Resource,
    create_list_from_input,
)

from src.helpers.image_helper import (
    get_media_file_creation_time,
    get_media_file_size,
)


def main() -> list[Resource]:
    all_resources: list[Resource] = []

    # define dataframe
    documentation_df = pd.read_excel("data/spreadsheets/Documentation.xlsx", dtype="str")

    # iterate through rows of dataframe:
    for _, row in documentation_df.iterrows():
        # define variables
        documentation_path = f"{row['Directory']}{row['File Name']}"
        timestamp_value = get_media_file_creation_time(documentation_path)
        file_size_value = get_media_file_size(documentation_path)
        authors = create_list_from_input(input_value=row["Authorship"], separator=",")
        authors_resource = create_list_from_input(input_value=row["Authorship Resource"], separator=",")

        # create resource, label and id
        resource = Resource.create_new(
            res_id=row["ID"],
            restype="project-medatada:Documentation",
            label=row["File Name"],
        )

        # add file to resource
        resource.add_file(
            documentation_path, license=LicenseRecommended.CC.BY, copyright_holder=row["Copyright"], authorship=authors
        )

        # add properties to resource
        resource.add_simpletext("project-medatada:hasID", row["ID"])
        resource.add_richtext("project-medatada:hasDescription", row["Description"])
        resource.add_simpletext("project-medatada:hasFileName", row["File Name"])
        resource.add_time_optional("project-medatada:hasTimeStamp", timestamp_value)
        resource.add_decimal_optional("project-medatada:hasFileSize", file_size_value)
        resource.add_simpletext("project-medatada:hasCopyrightResource", "DaSCH")
        resource.add_list("project-medatada:hasLicenseResource", "License", "LIC_002")
        resource.add_simpletext_multiple("project-medatada:hasAuthorshipResource", authors_resource)

        # append resource to list
        all_resources.append(resource)

    return all_resources


if __name__ == "__main__":
    main()
