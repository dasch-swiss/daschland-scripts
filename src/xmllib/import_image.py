import pandas as pd
from dsp_tools.xmllib import (
    LicenseRecommended,
    Permissions,
    Resource,
    create_list_from_input,
)

from src.helpers.cleaning_df_tools import create_list
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
        book_id = create_list(row["Book ID"])
        file_permissions = (
            Permissions.LIMITED_VIEW if row["Permission"] == "x" else Permissions.PROJECT_SPECIFIC_PERMISSIONS
        )
        authors = create_list_from_input(input_value=row["Authorship"], separator=",")

        # create resource, label and id
        resource = Resource.create_new(
            res_id=row["ID"],
            restype=":Image",
            label=row["Description"],
        )

        # add file to resource
        resource.add_file(
            filename=image_path,
            permissions=file_permissions,
            license=LicenseRecommended.DSP.PUBLIC_DOMAIN,
            copyright_holder=row["Copyright"],
            authorship=authors,
        )

        # add properties to resource
        resource.add_simpletext(value=row["ID"], prop_name=":hasID")
        resource.add_time_optional(value=timestamp_value, prop_name=":hasTimeStamp")
        resource.add_decimal_optional(value=file_size_value, prop_name=":hasFileSize")
        resource.add_simpletext("metadata:hasCopyright", "DaSCH")
        resource.add_list("metadata:hasLicenseList", "License", "CC BY 4.0")
        resource.add_simpletext_multiple("metadata:hasAuthorship", "Noémi Villars, Daniela Subotic")
        resource.add_simpletext(":hasFileName", row["File Name"])
        resource.add_link_multiple(":isPartOfBook", book_id)
        resource.add_integer(":hasSeqnum", row["Seqnum"])

        # append resource to list
        all_resources.append(resource)

    return all_resources


if __name__ == "__main__":
    main()
