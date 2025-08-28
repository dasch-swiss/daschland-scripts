import pandas as pd
from dsp_tools.xmllib import ListLookup, Resource, create_footnote_string, create_list_from_input

from src.helpers.helper import select_footnote_text


def main() -> list[Resource]:
    all_resources: list[Resource] = []

    # define json file path
    path_to_json = "daschland.json"

    # define dataframe
    character_df = pd.read_excel("data/spreadsheets/Character.xlsx", dtype="str")

    # create list mapping
    list_lookup = ListLookup.create_new(
        project_json_path=path_to_json,
        language_of_label="en",
        default_ontology="daschland",
    )

    # iterate through rows of dataframe:
    for _, row in character_df.iterrows():
        # define variables
        names = {row["Name EN"], row["Name DE"], row["Name FR"], row["Name IT"]}
        names = {name for name in names if pd.notna(name)}

        roles = create_list_from_input(row["Role List"], separator=",")
        image_ids = create_list_from_input(row["Image ID"], separator=",")

        keywords_names_raw = create_list_from_input(row["Keyword"], separator=",")
        keyword_names = [
            list_lookup.get_node_via_list_name(list_name="Keyword", node_label=x) for x in keywords_names_raw
        ]
        keyword_names = sorted(keyword_names)
        description_raw = row["Description"]
        footnote_text = select_footnote_text(description_raw)
        if footnote_text:
            footnote = create_footnote_string(footnote_text=footnote_text)
            description = description_raw.replace(f"*{footnote_text}*", footnote)
        else:
            description = description_raw
        authors_resource = create_list_from_input(input_value=row["Authorship Resource"], separator=",")

        # create resource, label and id
        resource = Resource.create_new(res_id=row["ID"], restype=":Character", label=row["Name EN"])

        # add properties to resource
        resource.add_simpletext(":hasID", row["ID"])
        resource.add_simpletext_multiple(":hasName", names)
        resource.add_richtext(":hasDescription", description)

        resource.add_richtext_optional(prop_name=":hasDescriptionAlternative", value=row["Alternative Description"])
        resource.add_list_multiple(prop_name=":hasRoleList", list_name="Role", values=roles)
        resource.add_richtext_optional(":hasQuote", row["Quote"])
        resource.add_link_multiple(":linkToImage", image_ids)
        resource.add_list_multiple(prop_name=":hasKeywordList", list_name="Keyword", values=keyword_names)
        resource.add_simpletext(":hasCopyrightResource", "DaSCH")
        resource.add_list(":hasLicenseResource", "License", "LIC_002")
        resource.add_simpletext_multiple(":hasAuthorshipResource", authors_resource)
        # append resource to list
        all_resources.append(resource)

    return all_resources


if __name__ == "__main__":
    main()
