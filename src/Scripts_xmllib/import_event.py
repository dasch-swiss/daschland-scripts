import pandas as pd
from dsp_tools.xmllib import (
    Resource,
    Permissions,
    create_label_to_name_list_node_mapping
)
from src.Helper_Scripts.cleaning_df_tools import create_list


def main():

    all_resources = []

    # define json file path
    path_to_json = "daschland.json"

    # define dataframe
    event_df = pd.read_excel("data/Spreadsheet_Data/Event.xlsx", dtype="str")

    # create mapping for lists
    event_label_to_names = create_label_to_name_list_node_mapping(
        project_json_path=path_to_json, list_name="Event Type", language_of_label="en"
    )

    # iterate through rows of dataframe:
    for _, row in event_df.iterrows():

        # define variables
        resource_id = row["ID"]
        resource_label = row["Name"]

        image_ids = create_list(row["Image ID"])
        event_type = event_label_to_names.get(row["Event Type List"])
        guest_ids = create_list(row["Guest ID"])
        protagonist_ids = create_list(row["Protagonist ID"])
        adventure_character_ids = create_list(row["Adventure Character ID"])
        antagonist_ids = create_list(row["Antagonist ID"])

        # create resource, label and id
        if row["Event Type"] == "Social":
            resource = Resource.create_new(
                res_id=resource_id, restype=":EventSocial", label=resource_label
            )
        elif row["Event Type"] == "Conflict":
            resource = Resource.create_new(
                res_id=resource_id, restype=":EventConflict", label=resource_label
            )
        elif row["Event Type"] == "Adventure":
            resource = Resource.create_new(
                res_id=resource_id, restype=":EventAdventure", label=resource_label
            )
        elif row["Event Type"] == "Alternative":
            resource = Resource.create_new(
                res_id=resource_id,
                restype=":EventAlternative",
                label=resource_label,
                permissions=Permissions.RESTRICTED,
            )
        else:
            continue

        # add properties to resource
        resource.add_simpletext(":hasID", resource_id)
        resource.add_simpletext(":hasName", row["Name"])
        resource.add_richtext(":hasDescription", row["Description"])
        resource.add_link_multiple(":linkToImage", image_ids)
        resource.add_list(":hasEventTypeList", "Event Type", event_type)

        # add properties for social event:
        resource.add_link_multiple(":linkToCharacter", guest_ids)
        resource.add_integer_optional(":hasGuestAmount", row["Guest Amount"])

        # add properties for conflict event:
        resource.add_link_multiple(":linkToCharacterProtagonist", protagonist_ids)
        resource.add_link_multiple(":linkToCharacterAntagonist", antagonist_ids)

        # add properties for adventure event:
        resource.add_link_multiple(":linkToCharacter", adventure_character_ids)
        resource.add_bool_optional(":isDangerous", row["Dangerous"])

        # add resource to list
        all_resources.append(resource)

    return all_resources


if __name__ == "__main__":
    main()
