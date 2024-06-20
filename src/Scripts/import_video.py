import pandas as pd
from dsp_tools import excel2xml
from src.Helper_Scripts import helper
from src.Helper_Scripts.image_helper import get_media_file_creation_time


def main():
    all_resources = []

    # define folder paths
    video_df = pd.read_excel("data/Spreadsheet_Data/Video.xlsx", dtype="str")

    # create the root element dsp-tools
    root = helper.make_root()

    # iterate through the rows of the old data from salsah:
    for _, row in video_df.iterrows():

        # create resource, label and id
        if not excel2xml.check_notna(row["ID"]):
            continue
        resource_id = row["ID"]
        resource_label = row["Label"]

        # create the `<resource>` tag
        resource = excel2xml.make_resource(
            label=resource_label,
            restype=":Video",
            id=resource_id)

        # create resource type "Image Human"
        video_path = f"{row['Directory']}{row['File Name']}"
        resource.append(excel2xml.make_bitstream_prop(video_path))

        if excel2xml.check_notna(row["ID"]):
            resource.append(excel2xml.make_text_prop(":hasID", resource_id))
        timestamp_value = get_media_file_creation_time(video_path)
        if excel2xml.check_notna(timestamp_value):
            resource.append(excel2xml.make_time_prop(":hasTimeStamp", timestamp_value))
        if excel2xml.check_notna(row["Copyright"]):
            resource.append(excel2xml.make_text_prop(":hasCopyright", row["Copyright"]))
        if excel2xml.check_notna(row["License List"]):
            resource.append(excel2xml.make_list_prop("License", ":hasLicenseList", row["License List"]))
        if excel2xml.check_notna(row["File Name"]):
            resource.append(excel2xml.make_text_prop(":hasFileName", row["File Name"]))
        if excel2xml.check_notna(row["Description"]):
            resource.append(excel2xml.make_text_prop(":hasDescription", excel2xml.PropertyElement(row["Description"], encoding="xml")))
        # append the resource to the list
        all_resources.append(resource)
    # add all resources to the root
    root.extend(all_resources)

    excel2xml.write_xml(root,
                        "data/XML/import_video.xml")
    return all_resources

if __name__ == "__main__":
    main()