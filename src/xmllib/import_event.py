import pandas as pd
from dsp_tools.xmllib import ListLookup, Resource, convert_to_bool_string, create_list_from_input, is_nonempty_value

from src.folder_paths import RAW_FOLDER


def main() -> list[Resource]:
    all_resources: list[Resource] = []

    # define json file path
    path_to_json = "daschland.json"

    # define dataframe
    event_df = pd.read_excel(RAW_FOLDER / "Event.xlsx", dtype="str")

    # create mapping for lists
    list_lookup = ListLookup.create_new(
        project_json_path=path_to_json,
        language_of_label="en",
        default_ontology="daschland",
    )

    # iterate through rows of dataframe:
    for _, row in event_df.iterrows():
        # define variables
        resource_id = row["ID"]
        resource_label = row["Name"]

        image_ids = create_list_from_input(row["Image ID"], separator=",")
        event_type = list_lookup.get_node_via_list_name(list_name="Event Type", node_label=row["Event Type List"])
        guest_ids = create_list_from_input(row["Guest ID"], separator=",")
        protagonist_ids = create_list_from_input(row["Protagonist ID"], separator=",")
        adventure_character_ids = create_list_from_input(row["Adventure Character ID"], separator=",")
        antagonist_ids = create_list_from_input(row["Antagonist ID"], separator=",")
        authors_resource = create_list_from_input(input_value=row["Authorship Resource"], separator=",")
        dangerous = convert_to_bool_string(row["Dangerous"]) if is_nonempty_value(row["Dangerous"]) else ""

        # create resource, label and id
        if row["Event Type"] == "Social":
            resource = Resource.create_new(res_id=resource_id, restype=":EventSocial", label=resource_label)
        elif row["Event Type"] == "Conflict":
            resource = Resource.create_new(res_id=resource_id, restype=":EventConflict", label=resource_label)
        elif row["Event Type"] == "Adventure":
            resource = Resource.create_new(res_id=resource_id, restype=":EventAdventure", label=resource_label)
        elif row["Event Type"] == "Alternative":
            resource = Resource.create_new(res_id=resource_id, restype=":EventAlternative", label=resource_label)
        else:
            continue

        # add properties to resource
        resource.add_simpletext("project-metadata:hasID", resource_id)
        resource.add_simpletext(":hasName", row["Name"])
        resource.add_richtext(":hasDescription", row["Description"])
        resource.add_link_multiple(":linkToImage", image_ids)
        resource.add_list_optional(":hasEventTypeList", "Event Type", event_type)

        # add properties for social event:
        resource.add_link_multiple(":linkToCharacter", guest_ids)
        resource.add_integer_optional(":hasGuestAmount", row["Guest Amount"])

        # add properties for conflict event:
        resource.add_link_multiple(":linkToCharacterProtagonist", protagonist_ids)
        resource.add_link_multiple(":linkToCharacterAntagonist", antagonist_ids)

        # add properties for adventure event:
        resource.add_link_multiple(":linkToCharacter", adventure_character_ids)
        resource.add_bool_optional(":isDangerous", dangerous)
        resource.add_simpletext("project-metadata:hasCopyrightResource", "DaSCH")
        resource.add_list("project-metadata:hasLicenseResource", "License", "LIC_002")
        resource.add_simpletext_multiple("project-metadata:hasAuthorshipResource", authors_resource)

        # add resource to list
        all_resources.append(resource)

    return all_resources


if __name__ == "__main__":
    main()
