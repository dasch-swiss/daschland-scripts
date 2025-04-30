import pandas as pd
from dsp_tools.xmllib import (
    LicenseRecommended,
    ListLookup,
    Resource,
    create_list_from_string,
)

from src.Helper_Scripts.image_helper import (
    get_media_file_creation_time,
    get_media_file_size,
)


def main() -> list[Resource]:
    all_resources: list[Resource] = []

    # define json file path
    path_to_json = "daschland.json"

    # define dataframe
    video_df = pd.read_excel("data/Spreadsheet_Data/Video.xlsx", dtype="str")

    # create list mapping
    list_lookup = ListLookup.create_new(
        project_json_path=path_to_json,
        language_of_label="en",
        default_ontology="daschland",
    )

    # iterate through rows of dataframe:
    for _, row in video_df.iterrows():
        # define variables
        video_path = f"{row['Directory']}{row['File Name']}"
        timestamp_value = get_media_file_creation_time(video_path)
        file_size_value = get_media_file_size(video_path)
        license_name = list_lookup.get_node_via_list_name(node_label=row["License List"], list_name="License")
        authors = create_list_from_string(string=row["Authorship"], separator=",")

        # create resource, label and id
        resource = Resource.create_new(
            res_id=row["ID"],
            restype=":Video",
            label=row["Label"],
        )

        # add file to resource
        resource.add_file(
            video_path,
            license=LicenseRecommended.DSP.PUBLIC_DOMAIN,
            copyright_holder=row["Copyright"],
            authorship=authors,
        )

        # add properties to resource
        resource.add_simpletext(":hasID", row["ID"])
        resource.add_time_optional(":hasTimeStamp", timestamp_value)
        resource.add_decimal_optional(":hasFileSize", file_size_value)
        resource.add_simpletext(":hasCopyright", row["Copyright"])
        resource.add_list(":hasLicenseList", "License", license_name)
        resource.add_simpletext(":hasFileName", row["File Name"])
        resource.add_richtext(":hasDescription", row["Description"])
        resource.add_richtext(":hasCast", row["Cast"])
        resource.add_simpletext_multiple(":hasAuthorship", row["Authorship"])

        # append resource to list
        all_resources.append(resource)

    return all_resources


if __name__ == "__main__":
    main()
