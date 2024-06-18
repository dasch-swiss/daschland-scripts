import pandas as pd
from dsp_tools import excel2xml
from src.Helper_Scripts import helper

def main():

    path_to_json = "daschland.json"
    all_resources = []

    # define folder paths
    character_df = pd.read_excel("data/Spreadsheet_Data/Character.xlsx", dtype="str")
    character_restricted_df = pd.read_excel("data/Spreadsheet_Data/CharacterRestricted.xlsx", dtype="str")

    # create mapping for lists
    role_label_to_names = excel2xml.create_json_list_mapping(
        path_to_json=path_to_json, list_name="Role", language_label="en"
    )
    education_grade_label_to_names = excel2xml.create_json_list_mapping(
        path_to_json=path_to_json, list_name="Education Grade", language_label="en"
    )
    department_label_to_names = excel2xml.create_json_list_mapping(
        path_to_json=path_to_json, list_name="Departement", language_label="en"
    )
    # create the root element dsp-tools
    root = helper.make_root()

    # iterate through the rows of the old data from salsah:
    for _, row in character_df.iterrows():

        # create resource, label and id
        if not excel2xml.check_notna(row["ID"]):
            continue
        resource_id = row["ID"]
        resource_label = f"{row["First Name"]} {row["Last Name"]}"

        # create the `<resource>` tag
        resource = excel2xml.make_resource(
            label=resource_label,
            restype=":Character",
            id=resource_id)

        # Append Properties
        if excel2xml.check_notna(row["ID"]):
            resource.append(excel2xml.make_text_prop(":hasID", resource_id))
        if excel2xml.check_notna(row["First Name"]):
            resource.append(excel2xml.make_text_prop(":hasFirstName", row["First Name"]))
        if excel2xml.check_notna(row["Last Name"]):
            resource.append(excel2xml.make_text_prop(":hasLastName", row["Last Name"]))
        if excel2xml.check_notna(row["Role List"]):
            roles_raw = [x.strip() for x in row["Role List"].split(",")]
            roles = [role_label_to_names.get(x) for x in roles_raw]
            resource.append(excel2xml.make_list_prop("Role", ":hasRoleList", roles))
        if excel2xml.check_notna(row["Quote"]):
            resource.append(excel2xml.make_text_prop(":hasQuote", excel2xml.PropertyElement(row["Quote"], encoding="xml")))

        if excel2xml.check_notna(row["Pet"]):
            resource.append(excel2xml.make_boolean_prop(":hasPet", row["Pet"]))
        if excel2xml.check_notna(row["Favorite Cake"]):
            resource.append(excel2xml.make_text_prop(":hasFavoriteCake", row["Favorite Cake"]))
        if excel2xml.check_notna(row["Education Grade List"]):
            education_grade = [x.strip() for x in row["Education Grade List"].split(",")]
            # education_grade = [education_grade_label_to_names.get(x) for x in education_grade_raw]
            resource.append(excel2xml.make_list_prop("Education Grade", ":hasEducationGradeList", education_grade))
        if excel2xml.check_notna(row["Departement List"]):
            department_raw = [x.strip() for x in row["Departement List"].split(",")]
            department = [department_label_to_names.get(x) for x in department_raw]
            resource.append(excel2xml.make_list_prop("Departement", ":hasDepartementList", department))

        # Append link Properties
        if excel2xml.check_notna(row["Link to Image ID"]):
            linkToImageID = [x.strip() for x in row["Link to Image ID"].split(",")]
            resource.append(excel2xml.make_resptr_prop(":linkToImageID", linkToImageID))

        if excel2xml.check_notna(row["Link To Alice Character ID"]):
            alice_id = [x.strip() for x in row["Link To Alice Character ID"].split(",")]
            resource.append(excel2xml.make_resptr_prop(":linkToAliceCharacterID", alice_id))

        for _, row in character_restricted_df.iterrows():
            if row["ID"] == resource_id and excel2xml.check_notna(row["Birthday"]):
                birthday = excel2xml.find_date_in_string(row["Birthday"])
                resource.append(excel2xml.make_date_prop(":hasBirthday", excel2xml.PropertyElement(birthday, permissions = "res-restricted")))

        # append the resource to the list
        all_resources.append(resource)
    # add all resources to the root
    root.extend(all_resources)

    excel2xml.write_xml(root,
                        "data/XML/import_character.xml")
    return all_resources

if __name__ == "__main__":
    main()










