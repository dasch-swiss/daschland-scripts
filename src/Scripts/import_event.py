
import pandas as pd
from dsp_tools import excel2xml
from src.Helper_Scripts import helper
from src.Helper_Scripts.image_helper import get_media_file_creation_time


def main():
    all_resources = []
    path_to_json = "daschland.json"

    # define folder paths
    event_df = pd.read_excel("data/Spreadsheet_Data/Event.xlsx", dtype="str")

    # create mapping for lists
    location_label_to_names = excel2xml.create_json_list_mapping(
        path_to_json=path_to_json, list_name="Wonderland Location", language_label="en"
    )
    # create the root element dsp-tools
    root = helper.make_root()

    # iterate through the rows of the old data from salsah:
    for _, row in event_df.iterrows():

        # create resource, label and id
        if not excel2xml.check_notna(row["ID"]):
            continue
        resource_id = row["ID"]
        resource_label = row["Name"]

        # create the `<resource>` tag
        if row["Event Type List"] == "Social":
            resource = excel2xml.make_resource(
                label=resource_label,
                restype=":EventSocial",
                id=resource_id)
        elif row["Event Type List"] == "Conflict":
            resource = excel2xml.make_resource(
                label=resource_label,
                restype=":EventConflict",
                id=resource_id)
        elif row["Event Type List"] == "Adventure":
            resource = excel2xml.make_resource(
                label=resource_label,
                restype=":Adventure",
                id=resource_id)

        #append Properties
        if excel2xml.check_notna(row["ID"]):
            resource.append(excel2xml.make_text_prop(":hasID", resource_id))
        if excel2xml.check_notna(row["Name"]):
            resource.append(excel2xml.make_text_prop(":hasName", row["Name"]))
        if excel2xml.check_notna(row["Description"]):
            resource.append(excel2xml.make_text_prop(":hasDescription", row["Description"]))
        if excel2xml.check_notna(row["Location ID"]):
            location_ids = [x.strip() for x in row["Location ID"].split(",")]
            resource.append(excel2xml.make_resptr_prop(":linkToLocationID", location_ids))

        # append properties for social event:
        if excel2xml.check_notna(row["Guest ID"]):
            guest_ids = [x.strip() for x in row["Guest ID"].split(",")]
            resource.append(excel2xml.make_resptr_prop(":linkToCharacterID", guest_ids))
        if excel2xml.check_notna(row["Guest Amount"]):
            resource.append(excel2xml.make_integer_prop(":hasGuestAmount", row["Guest Amount"]))

        # append properties for conflict event:
        if excel2xml.check_notna(row["Protagonist ID"]):
            protagonist_ids = [x.strip() for x in row["Protagonist ID"].split(",")]
            resource.append(excel2xml.make_resptr_prop(":linkToCharacterProtagonistID", protagonist_ids))
        if excel2xml.check_notna(row["Antagonist ID"]):
            antagonist_ids = [x.strip() for x in row["Antagonist ID"].split(",")]
            resource.append(excel2xml.make_resptr_prop(":linkToCharacterAntagonistID", antagonist_ids))

        # append properties for adventure event:
        if excel2xml.check_notna(row["Adventure Character ID"]):
            adventure_character_ids = [x.strip() for x in row["Adventure Character ID"].split(",")]
            resource.append(excel2xml.make_resptr_prop(":linkToCharacterID", adventure_character_ids))
        if excel2xml.check_notna(row["Adventure Type List"]):
            adventure_type = location_label_to_names.get(row["Adventure Type List"])
            resource.append(excel2xml.make_list_prop("Adventure Type", ":hasAdventureTypeList", adventure_type))
        if excel2xml.check_notna(row["Dangerous"]):
            resource.append(excel2xml.make_boolean_prop(":isDangerous", row["Dangerous"]))

        # append the resource to the list
        all_resources.append(resource)
    # add all resources to the root
    root.extend(all_resources)

    excel2xml.write_xml(root,
                        "data/XML/import_event.xml")
    return all_resources

if __name__ == "__main__":
    main()