
import pandas as pd
from dsp_tools import excel2xml
from src.Helper_Scripts import helper
from src.Helper_Scripts.image_helper import get_media_file_creation_time


def main():
    all_resources = []
    path_to_json = "daschland.json"

    # define folder paths
    location_df = pd.read_excel("data/Spreadsheet_Data/Location.xlsx", dtype="str")

    # create mapping for lists
    location_label_to_names = excel2xml.create_json_list_mapping(
        path_to_json=path_to_json, list_name="Fairytale Location", language_label="en"
    )
    # create the root element dsp-tools
    root = helper.make_root()

    # iterate through the rows of the old data from salsah:
    for _, row in location_df.iterrows():

        # create resource, label and id
        if not excel2xml.check_notna(row["ID"]):
            continue
        resource_id = row["ID"]
        resource_label = row["Name"]

        # create the `<resource>` tag
        if row["Location Type List"] == "Real World":
            resource = excel2xml.make_resource(
                label=resource_label,
                restype=":LocationRealWorld",
                id=resource_id)
        elif row["Location Type List"] == "Wonderland":
            resource = excel2xml.make_resource(
                label=resource_label,
                restype=":LocationWonderland",
                id=resource_id)
        else:
            resource = excel2xml.make_resource(
                label=resource_label,
                restype=":Location",
                id=resource_id)

        #append Properties
        if excel2xml.check_notna(row["ID"]):
            resource.append(excel2xml.make_text_prop(":hasID", resource_id))
        if excel2xml.check_notna(row["Name"]):
            resource.append(excel2xml.make_text_prop(":hasName", row["Name"]))
        if excel2xml.check_notna(row["Description"]):
            resource.append(excel2xml.make_text_prop(":hasDescription", excel2xml.PropertyElement(row["Description"], encoding="xml")))

        # append Properties for Real World Locations:
        if excel2xml.check_notna(row["Geoname ID"]):
            resource.append(excel2xml.make_geoname_prop(":hasGeoname", row["Geoname ID"]))

        # append the resource to the list
        all_resources.append(resource)
    # add all resources to the root
    root.extend(all_resources)

    excel2xml.write_xml(root,
                        "data/XML/import_location.xml")
    return all_resources

if __name__ == "__main__":
    main()