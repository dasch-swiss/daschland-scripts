import pandas as pd
from dsp_tools import excel2xml

from src.Helper_Scripts import helper_excel2xml


def main():
    all_resources = []

    # create the root element dsp-tools
    root = helper_excel2xml.make_root()

    # define dataframe
    location_df = pd.read_excel("data/Spreadsheet_Data/Location.xlsx", dtype="str")

    # iterate through rows of dataframe:
    for _, row in location_df.iterrows():
        # define variables
        resource_id = row["ID"]
        resource_label = row["Name"]
        descriptions = [row["Description EN"], row["Description DE"], row["Description FR"], row["Description IT"]]
        descriptions = [description for description in descriptions if pd.notna(description)]

        # create resource, label and id
        if not excel2xml.check_notna(row["ID"]):
            continue

        if row["Location Type List"] == "Real World":
            resource = excel2xml.make_resource(label=resource_label, restype=":LocationRealWorld", id=resource_id)
        elif row["Location Type List"] == "Wonderland":
            resource = excel2xml.make_resource(label=resource_label, restype=":LocationWonderland", id=resource_id)
        else:
            resource = excel2xml.make_resource(label=resource_label, restype=":Location", id=resource_id)

        # add properties to resource
        if excel2xml.check_notna(row["ID"]):
            resource.append(excel2xml.make_text_prop(":hasID", resource_id))
        if excel2xml.check_notna(row["Name"]):
            resource.append(excel2xml.make_text_prop(":hasName", row["Name"]))
        if descriptions:
            text_elements = []
            for description in descriptions:
                text_element = excel2xml.PropertyElement(description, encoding="xml")
                text_elements.append(text_element)
            resource.append(excel2xml.make_text_prop(":hasDescription", text_elements))
        if excel2xml.check_notna(row["Image ID"]):
            image_ids = [x.strip() for x in row["Image ID"].split(",")]
            resource.append(excel2xml.make_resptr_prop(":linkToImage", image_ids))

        # append Properties for Real World Locations:
        if excel2xml.check_notna(row["Geoname ID"]):
            resource.append(excel2xml.make_geoname_prop(":hasGeoname", row["Geoname ID"]))

        # append the resource to the list
        all_resources.append(resource)

    # add all resources to the root
    root.extend(all_resources)

    # write root to xml file
    excel2xml.write_xml(root, "data/XML/import_location.xml")
    return all_resources


if __name__ == "__main__":
    main()
