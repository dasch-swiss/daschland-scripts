import pandas as pd
from dsp_tools.xmllib import ListLookup, Permissions, Resource
from dsp_tools.xmllib.helpers import create_footnote_string

from src.Helper_Scripts.cleaning_df_tools import create_list
from src.Helper_Scripts.helper import select_footnote_text


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

        roles = create_list(row["Role List"])
        image_ids = create_list(row["Image ID"])

        keywords_names_raw = create_list(row["Keyword"])
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

        # create resource, label and id
        resource = Resource.create_new(res_id=row["ID"], restype=":Character", label=row["Name EN"])

        # add properties to resource
        resource.add_simpletext(":hasID", row["ID"])
        resource.add_simpletext_multiple(":hasName", names)
        resource.add_richtext(":hasDescription", description)

        resource.add_richtext_optional(
            prop_name=":hasDescriptionAlternative",
            value=row["Alternative Description"],
            permissions=Permissions.RESTRICTED,
        )
        resource.add_list_multiple(prop_name=":hasRoleList", list_name="Role", values=roles)
        resource.add_richtext_optional(":hasQuote", row["Quote"])
        resource.add_link_multiple(":linkToImage", image_ids)
        resource.add_list_multiple(prop_name=":hasKeywordList", list_name="Keyword", values=keyword_names)

        # append resource to list
        all_resources.append(resource)

    return all_resources


if __name__ == "__main__":
    main()
