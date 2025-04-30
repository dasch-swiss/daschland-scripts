import pandas as pd
from dsp_tools.xmllib import (
    Resource,
    Permissions,
    ListLookup,
    create_list_from_string,
    LicenseRecommended,
)
from src.Helper_Scripts.image_helper import get_image_creation_time, get_media_file_size
from src.Helper_Scripts.cleaning_df_tools import create_list


def main():
    all_resources = []

    # define json file path
    path_to_json = "daschland.json"

    # define dataframe
    image_df = pd.read_excel("data/Spreadsheet_Data/Image.xlsx", dtype="str")

    # create list mapping
    list_lookup = ListLookup.create_new(
        project_json_path=path_to_json,
        language_of_label="en",
        default_ontology="daschland",
    )

    # iterate through rows of dataframe:
    for _, row in image_df.iterrows():
        # define variables
        image_path = f"{row['Directory']}{row['File Name']}"
        timestamp_value = get_image_creation_time(image_path)
        file_size_value = get_media_file_size(image_path)
        license_name = list_lookup.get_node_via_list_name(node_label=row["License List"], list_name="License")
        book_id = create_list(row["Book ID"])
        file_permissions = (
            Permissions.RESTRICTED_VIEW if row["Permission"] == "x" else Permissions.PROJECT_SPECIFIC_PERMISSIONS
        )
        authors = create_list_from_string(string=row["Authorship"], separator=",")

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
        resource.add_decimal(value=file_size_value, prop_name=":hasFileSize")
        resource.add_simpletext(":hasCopyright", row["Copyright"])
        resource.add_list(":hasLicenseList", "License", license_name)
        resource.add_simpletext(":hasFileName", row["File Name"])
        resource.add_link_multiple(":isPartOfBook", book_id)
        resource.add_integer(":hasSeqnum", row["Seqnum"])
        resource.add_simpletext_multiple(":hasAuthorship", row["Authorship"])

        # append resource to list
        all_resources.append(resource)

    return all_resources


if __name__ == "__main__":
    main()
