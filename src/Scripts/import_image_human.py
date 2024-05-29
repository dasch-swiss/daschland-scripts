import pandas as pd
from dsp_tools import excel2xml
from src.Helper_Scripts import helper
from src.Helper_Scripts.image_helper import get_image_creation_time


def main():
    all_resources = []

    # define folder paths
    image_human_df = pd.read_excel("~/documents/daschland-scripts/data/Spreadsheet_Data/ImagesHuman.xlsx", dtype="str")

    # create the root element dsp-tools
    root = helper.make_root()

    # iterate through the rows of the old data from salsah:
    for _, row in image_human_df.iterrows():

        # create resource, label and id
        if not excel2xml.check_notna(row["hasID"]):
            continue
        resource_id = row["hasID"]
        resource_label = row["Label"]

        # create the `<resource>` tag
        resource = excel2xml.make_resource(
            label=resource_label,
            restype=":ImageHuman",
            id=resource_id)

        # create resource type "Image Human"
        image_path = f"{row['ImageDirectory']}{row['hasFilename']}"
        resource.append(excel2xml.make_bitstream_prop(image_path))

        if excel2xml.check_notna(row["hasID"]):
            resource.append(excel2xml.make_text_prop(":hasID", resource_id))
        timestamp_value = get_image_creation_time(image_path)
        if excel2xml.check_notna(timestamp_value):
            resource.append(excel2xml.make_time_prop(":hasTimeStamp", timestamp_value))
        if excel2xml.check_notna(row["hasCopyright"]):
            resource.append(excel2xml.make_text_prop(":hasCopyright", row["hasCopyright"]))
        if excel2xml.check_notna(row["hasLicenseList"]):
            resource.append(excel2xml.make_list_prop("License", ":hasLicenseList", row["hasLicenseList"]))
        if excel2xml.check_notna(row["hasFilename"]):
            resource.append(excel2xml.make_text_prop(":hasFileName", row["hasFilename"]))

        # append the resource to the list
        all_resources.append(resource)
    # add all resources to the root
    root.extend(all_resources)

    excel2xml.write_xml(root,
                        "/Users/noemivillars-amberg/Documents/daschland-scripts/data/XML/import_image_human.xml")
    return all_resources


if __name__ == "__main__":
    main()
