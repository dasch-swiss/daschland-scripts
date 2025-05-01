import pandas as pd
from dsp_tools import excel2xml

from src.Helper_Scripts import helper_excel2xml


def main():
    all_resources = []

    # define json file path
    path_to_json = "daschland.json"

    # create the root element dsp-tools
    root = helper_excel2xml.make_root()

    # define dataframe
    event_df = pd.read_excel("data/spreadsheets/Event.xlsx", dtype="str")

    # create list mapping
    event_label_to_names = excel2xml.create_json_list_mapping(
        path_to_json=path_to_json, list_name="Event Type", language_label="en"
    )

    # iterate through rows of dataframe:
    for _, row in event_df.iterrows():
        # define variables
        resource_id = row["ID"]
        resource_label = row["Name"]

        # create resource, label and id
        if not excel2xml.check_notna(row["ID"]):
            continue

        if row["Event Type"] == "Social":
            resource = excel2xml.make_resource(label=resource_label, restype=":EventSocial", id=resource_id)
        elif row["Event Type"] == "Conflict":
            resource = excel2xml.make_resource(label=resource_label, restype=":EventConflict", id=resource_id)
        elif row["Event Type"] == "Adventure":
            resource = excel2xml.make_resource(label=resource_label, restype=":EventAdventure", id=resource_id)
        elif row["Event Type"] == "Alternative":
            resource = excel2xml.make_resource(
                label=resource_label,
                restype=":EventAlternative",
                permissions="res-restricted",
                id=resource_id,
            )
        else:
            continue

        # add properties to resource
        if excel2xml.check_notna(row["ID"]):
            resource.append(excel2xml.make_text_prop(":hasID", resource_id))
        if excel2xml.check_notna(row["Name"]):
            resource.append(excel2xml.make_text_prop(":hasName", row["Name"]))
        if excel2xml.check_notna(row["Description"]):
            resource.append(
                excel2xml.make_text_prop(
                    ":hasDescription",
                    excel2xml.PropertyElement(row["Description"], encoding="xml"),
                )
            )
        if excel2xml.check_notna(row["Image ID"]):
            image_ids = [x.strip() for x in row["Image ID"].split(",")]
            resource.append(excel2xml.make_resptr_prop(":linkToImage", image_ids))
        if excel2xml.check_notna(row["Event Type List"]):
            event_type = event_label_to_names.get(row["Event Type List"])
            resource.append(excel2xml.make_list_prop("Event Type", ":hasEventTypeList", event_type))

        # append properties for social event:
        if excel2xml.check_notna(row["Guest ID"]):
            guest_ids = [x.strip() for x in row["Guest ID"].split(",")]
            resource.append(excel2xml.make_resptr_prop(":linkToCharacter", guest_ids))
        if excel2xml.check_notna(row["Guest Amount"]):
            resource.append(excel2xml.make_integer_prop(":hasGuestAmount", row["Guest Amount"]))

        # append properties for conflict event:
        if excel2xml.check_notna(row["Protagonist ID"]):
            protagonist_ids = [x.strip() for x in row["Protagonist ID"].split(",")]
            resource.append(excel2xml.make_resptr_prop(":linkToCharacterProtagonist", protagonist_ids))
        if excel2xml.check_notna(row["Antagonist ID"]):
            antagonist_ids = [x.strip() for x in row["Antagonist ID"].split(",")]
            resource.append(excel2xml.make_resptr_prop(":linkToCharacterAntagonist", antagonist_ids))

        # append properties for adventure event:
        if excel2xml.check_notna(row["Adventure Character ID"]):
            adventure_character_ids = [x.strip() for x in row["Adventure Character ID"].split(",")]
            resource.append(excel2xml.make_resptr_prop(":linkToCharacter", adventure_character_ids))
        if excel2xml.check_notna(row["Dangerous"]):
            resource.append(excel2xml.make_boolean_prop(":isDangerous", row["Dangerous"]))

        # append the resource to the list
        all_resources.append(resource)

    # add all resources to the root
    root.extend(all_resources)

    # write root to xml file
    excel2xml.write_xml(root, "data/xml/import_event.xml")
    return all_resources


if __name__ == "__main__":
    main()
