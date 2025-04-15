import pandas as pd
from dsp_tools.xmllib import Resource, create_label_to_name_list_node_mapping, LicenseRecommended, create_list_from_string
from src.Helper_Scripts.image_helper import get_media_file_creation_time


def main():
    all_resources = []

    # define json file path
    path_to_json = "daschland.json"

    # define dataframe
    book_df = pd.read_excel("data/Spreadsheet_Data/BookEdition.xlsx", dtype="str")

    # create list mapping
    license_labels_to_names = create_label_to_name_list_node_mapping(
        project_json_path=path_to_json,
        list_name="License",
        language_of_label="en",
    )

    # iterate through rows of dataframe:
    for _, row in book_df.iterrows():

        # define variables
        book_path = f"{row['Directory']}{row['File Name']}"
        timestamp_value = get_media_file_creation_time(book_path)
        license_name = license_labels_to_names.get(row["License List"])
        authors = create_list_from_string(string=row["Authorship"], separator=",")

        # create resource, label and id
        resource = Resource.create_new(
            res_id=row["ID"], restype=":BookEdition", label=row["File Name"]
        )

        # add file to resource
        resource.add_file(filename=book_path, license=LicenseRecommended.DSP.PUBLIC_DOMAIN, copyright_holder=row["Copyright"], authorship=authors)

        # add properties to resource
        resource.add_simpletext(":hasID", row["ID"])
        resource.add_simpletext(":hasFileName", row["File Name"])
        resource.add_richtext(":hasDescription", row["Description"])
        resource.add_time_optional(":hasTimeStamp", timestamp_value)
        resource.add_simpletext(":hasCopyright", row["Copyright"])
        resource.add_list(":hasLicenseList", "License", license_name)
        resource.add_simpletext_multiple(":hasAuthorship", row["Authorship"])

        # append resource to list
        all_resources.append(resource)

    return all_resources


if __name__ == "__main__":
    main()
