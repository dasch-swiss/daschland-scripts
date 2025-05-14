import pandas as pd
from dsp_tools import excel2xml

from src.helpers import helper_excel2xml
from src.helpers.image_helper import (
    get_media_file_creation_time,
    get_media_file_size,
)


def main():
    all_resources = []

    # define json file path
    path_to_json = "daschland.json"

    # create the root element dsp-tools
    root = helper_excel2xml.make_root()

    # define dataframe
    audio_df = pd.read_excel("data/spreadsheets/Audio.xlsx", dtype="str")

    # create list mapping
    license_labels_to_names = excel2xml.create_json_list_mapping(
        path_to_json=path_to_json,
        list_name="License",
        language_label="en",
    )

    # iterate through rows of dataframe:
    for _, row in audio_df.iterrows():
        # define variables
        resource_id = row["ID"]
        resource_label = row["Name"]
        audio_path = f"{row['Directory']}{row['File Name']}"
        timestamp_value = get_media_file_creation_time(audio_path)
        file_size_value = get_media_file_size(audio_path)

        # create resource, label and id
        if not excel2xml.check_notna(row["ID"]):
            continue

        resource = excel2xml.make_resource(label=resource_label, restype=":Audio", id=resource_id)

        # add file to resource
        resource.append(excel2xml.make_bitstream_prop(audio_path))

        # add properties to resource
        if excel2xml.check_notna(row["ID"]):
            resource.append(excel2xml.make_text_prop(":hasID", resource_id))
        if excel2xml.check_notna(timestamp_value):
            resource.append(excel2xml.make_time_prop(":hasTimeStamp", timestamp_value))
        if excel2xml.check_notna(file_size_value):
            resource.append(excel2xml.make_decimal_prop(":hasFileSize", file_size_value))
        if excel2xml.check_notna(row["Copyright"]):
            resource.append(excel2xml.make_text_prop(":hasCopyright", row["Copyright"]))
        if excel2xml.check_notna(row["License List"]):
            license_name = license_labels_to_names[row["License List"]]
            resource.append(excel2xml.make_list_prop("License", ":hasLicenseList", license_name))
        if excel2xml.check_notna(row["File Name"]):
            resource.append(excel2xml.make_text_prop(":hasFileName", row["File Name"]))
        if excel2xml.check_notna(row["Description"]):
            resource.append(
                excel2xml.make_text_prop(
                    ":hasDescription",
                    excel2xml.PropertyElement(row["Description"], encoding="xml"),
                )
            )
        if excel2xml.check_notna(row["Cast"]):
            resource.append(
                excel2xml.make_text_prop(":hasCast", excel2xml.PropertyElement(row["Cast"], encoding="xml"))
            )
        if excel2xml.check_notna(row["Authorship"]):
            authorship = [x.strip() for x in row["Authorship"].split(",")]
            resource.append(excel2xml.make_text_prop(":hasAuthorship", authorship))

        # append the resource to the list
        all_resources.append(resource)

    # add all resources to the root
    root.extend(all_resources)

    # write root to xml file
    return all_resources


if __name__ == "__main__":
    main()
