import pandas as pd
from dsp_tools import excel2xml

from src.helpers import helper_excel2xml


def main():
    all_resources = []

    # define json file path
    path_to_json = "daschland.json"

    # create the root element dsp-tools
    root = helper_excel2xml.make_root()

    # define dataframe
    character_df = pd.read_excel("data/spreadsheets/Character.xlsx", dtype="str")

    # create list mapping
    keyword_labels_to_names = excel2xml.create_json_list_mapping(
        path_to_json=path_to_json,
        list_name="Keyword",
        language_label="en",
    )

    # iterate through rows of dataframe:
    for _, row in character_df.iterrows():
        # define variables
        resource_id = row["ID"]
        resource_label = row["Name EN"]
        names = {row["Name EN"], row["Name DE"], row["Name FR"], row["Name IT"]}
        names = {name for name in names if pd.notna(name)}

        # create resource, label and id
        if not excel2xml.check_notna(row["ID"]):
            continue

        resource = excel2xml.make_resource(label=resource_label, restype=":Character", id=resource_id)

        # add properties to resource
        if excel2xml.check_notna(row["ID"]):
            resource.append(excel2xml.make_text_prop(":hasID", resource_id))
        if names:
            resource.append(excel2xml.make_text_prop(":hasName", names))
        if excel2xml.check_notna(row["Description"]):
            resource.append(
                excel2xml.make_text_prop(
                    ":hasDescription",
                    excel2xml.PropertyElement(row["Description"], encoding="xml"),
                )
            )
        if excel2xml.check_notna(row["Alternative Description"]):
            resource.append(
                excel2xml.make_text_prop(
                    ":hasDescriptionAlternative",
                    excel2xml.PropertyElement(
                        row["Alternative Description"],
                        encoding="xml",
                        permissions="prop-restricted",
                    ),
                )
            )
        if excel2xml.check_notna(row["Colour"]):
            color = [x.strip() for x in row["Colour"].split(",")]
            resource.append(excel2xml.make_color_prop(":hasColour", color))
        if excel2xml.check_notna(row["Role List"]):
            roles = [x.strip() for x in row["Role List"].split(",")]
            resource.append(excel2xml.make_list_prop("Role", ":hasRoleList", roles))
        if excel2xml.check_notna(row["Quote"]):
            resource.append(
                excel2xml.make_text_prop(":hasQuote", excel2xml.PropertyElement(row["Quote"], encoding="xml"))
            )
        if excel2xml.check_notna(row["Image ID"]):
            image_ids = [x.strip() for x in row["Image ID"].split(",")]
            resource.append(excel2xml.make_resptr_prop(":linkToImage", image_ids))
        if excel2xml.check_notna(row["Keyword"]):
            keywords_names_raw = [x.strip() for x in row["Keyword"].split(",")]
            for keyword in keywords_names_raw:
                if keyword not in keyword_labels_to_names:
                    print(f"Keyword {keyword} - {resource_label} not found in the json file.")
                    continue
            keyword_names = [keyword_labels_to_names.get(x) for x in keywords_names_raw]
            keyword_names = sorted(keyword_names)
            resource.append(
                excel2xml.make_list_prop(
                    "Keyword",
                    ":hasKeywordList",
                    keyword_names,
                    calling_resource=row["ID"],
                )
            )

        # append the resource to the list
        all_resources.append(resource)

    # add all resources to the root
    root.extend(all_resources)

    # write root to xml file
    excel2xml.write_xml(root, "data/xml/import_character.xml")
    return all_resources


if __name__ == "__main__":
    main()
