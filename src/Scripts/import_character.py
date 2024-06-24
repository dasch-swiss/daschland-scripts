import pandas as pd
from dsp_tools import excel2xml
from src.Helper_Scripts import helper

def main():
    path_to_json = "daschland.json"

    all_resources = []

    # define folder paths
    character_df = pd.read_excel("data/Spreadsheet_Data/Character.xlsx", dtype="str")

    # create mapping for lists
    role_label_to_names = excel2xml.create_json_list_mapping(
        path_to_json=path_to_json, list_name="Role", language_label="en"
    )

    # create the root element dsp-tools
    root = helper.make_root()

    # iterate through the rows of the old data from salsah:
    for _, row in character_df.iterrows():

        # create resource, label and id
        if not excel2xml.check_notna(row["ID"]):
            continue
        resource_id = row["ID"]
        resource_label = row["Name"]

        # create the `<resource>` tag
        resource = excel2xml.make_resource(
            label=resource_label,
            restype=":Character",
            id=resource_id)

        # Append Properties
        if excel2xml.check_notna(row["ID"]):
            resource.append(excel2xml.make_text_prop(":hasID", resource_id))
        if excel2xml.check_notna(row["Name"]):
            resource.append(excel2xml.make_text_prop(":hasName", row["Name"]))
        if excel2xml.check_notna(row["Description"]):
            resource.append(excel2xml.make_text_prop(":hasDescription", excel2xml.PropertyElement(row["Description"], encoding="xml")))
        if excel2xml.check_notna(row["Colour"]):
            color = [x.strip() for x in row["Colour"].split(",")]
            resource.append(excel2xml.make_color_prop(":hasColor", color))
        if excel2xml.check_notna(row["Role List"]):
            roles = [x.strip() for x in row["Role List"].split(",")]
            # roles = [role_label_to_names.get(x) for x in roles_raw]
            resource.append(excel2xml.make_list_prop("Role", ":hasRoleList", roles))
        if excel2xml.check_notna(row["Quote"]):
            resource.append(excel2xml.make_text_prop(":hasQuote", excel2xml.PropertyElement(row["Quote"], encoding="xml")))

        # append the resource to the list
        all_resources.append(resource)
    # add all resources to the root
    root.extend(all_resources)

    excel2xml.write_xml(root,
                        "data/XML/import_character.xml")
    return all_resources

if __name__ == "__main__":
    main()










