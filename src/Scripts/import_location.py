
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
        path_to_json=path_to_json, list_name="Wonderland Location", language_label="en"
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
        resource = excel2xml.make_resource(
            label=resource_label,
            restype=":Location",
            id=resource_id)

        #append Properties
        if excel2xml.check_notna(row["ID"]):
            resource.append(excel2xml.make_text_prop(":hasID", resource_id))
        if excel2xml.check_notna(row["Geoname"]):
            resource.append(excel2xml.make_geoname_prop(":hasGeoname", row["Geoname"]))
        if excel2xml.check_notna(row["Wonderland Location List"]):
            wonderland_location = location_label_to_names.get(row["Wonderland Location List"])
            resource.append(excel2xml.make_list_prop("Wonderland Location", ":hasWonderlandLocationList", wonderland_location))
        if excel2xml.check_notna(row["Name"]):
            resource.append(excel2xml.make_text_prop(":hasFileName", row["Name"]))

        # append the resource to the list
        all_resources.append(resource)
    # add all resources to the root
    root.extend(all_resources)

    excel2xml.write_xml(root,
                        "data/XML/import_location.xml")
    return all_resources

if __name__ == "__main__":
    main()