import pandas as pd
from dsp_tools.xmllib import (
    Resource,
    create_label_to_name_list_node_mapping,
    LicenseRecommended,
    create_list_from_string,
)
from src.Helper_Scripts.image_helper import (
    get_media_file_size,
    get_media_file_creation_time,
)


def main() -> list[Resource]:
    all_resources: list[Resource] = []

    # define json file path
    path_to_json = "daschland.json"

    # define dataframe
    archive_df = pd.read_excel("data/Spreadsheet_data/Archive.xlsx")

    # create list mapping
    license_labels_to_names = create_label_to_name_list_node_mapping(
        project_json_path=path_to_json, list_name="License", language_of_label="en"
    )

    # iterate through rows of dataframe:
    for _, row in archive_df.iterrows():
        # define variables
        archive_path = f"{row['Directory']}{row['File Name']}"
        timestamp_value = get_media_file_creation_time(archive_path)
        file_size_value = get_media_file_size(archive_path)
        license_name = license_labels_to_names.get(row["License List"])
        authors = create_list_from_string(string=row["Authorship"], separator=",")

        # create resource, label and id
        resource = Resource.create_new(res_id=row["ID"], restype="metadata:Archive", label=row["File Name"])

        # add file to resource
        resource.add_file(
            filename=archive_path,
            license=LicenseRecommended.CC.BY,
            copyright_holder=row["Copyright"],
            authorship=authors,
        )

        # add properties to resource
        resource.add_simpletext("metadata:hasID", row["ID"])
        resource.add_richtext("metadata:hasDescription", row["Description"])
        resource.add_simpletext("metadata:hasFileName", row["File Name"])
        resource.add_time_optional("metadata:hasTimeStamp", timestamp_value)
        resource.add_decimal_optional("metadata:hasFileSize", file_size_value)
        resource.add_simpletext("metadata:hasCopyright", row["Copyright"])
        resource.add_list_optional("metadata:hasLicenseList", "License", license_name)
        resource.add_simpletext_multiple("metadata:hasAuthorship", row["Authorship"])

        # append resource to list
        all_resources.append(resource)

    return all_resources


if __name__ == "__main__":
    main()
