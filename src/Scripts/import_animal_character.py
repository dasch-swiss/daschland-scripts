import pandas as pd
from dsp_tools import excel2xml
from src.Helper_Scripts import helper

def main():
    all_resources = []

    # define folder paths
    animal_character_df = pd.read_excel("data/Spreadsheet_Data/AnimalCharacter.xlsx", dtype="str")

    # create the root element dsp-tools
    root = helper.make_root()

    # iterate through the rows of the old data from salsah:
    for _, row in animal_character_df.iterrows():

        # create resource, label and id
        if not excel2xml.check_notna(row["ID"]):
            continue
        resource_id = row["ID"]
        resource_label = row["Short Name"]

        # create the `<resource>` tag
        resource = excel2xml.make_resource(
            label=resource_label,
            restype=":AnimalCharacter",
            id=resource_id)

        # Append Properties
        if excel2xml.check_notna(row["ID"]):
            resource.append(excel2xml.make_text_prop(":hasID", resource_id))
        if excel2xml.check_notna(row["Description"]):
            resource.append(excel2xml.make_text_prop(":hasDescription", excel2xml.PropertyElement(row["Description"], encoding="xml")))
        if excel2xml.check_notna(row["Short Name"]):
            resource.append(excel2xml.make_text_prop(":hasShortName", row["Short Name"]))
        if excel2xml.check_notna(row["Pet Color"]):
            color = [x.strip() for x in row["Pet Color"].split(",")]
            resource.append(excel2xml.make_color_prop(":hasPetColor", color))
        if excel2xml.check_notna(row["Specie List"]):
            resource.append(excel2xml.make_list_prop("Specie", ":hasSpecieList", row["Specie List"]))
        if excel2xml.check_notna(row["Gender List"]):
            resource.append(excel2xml.make_list_prop("Gender", ":hasGenderList", row["Gender List"]))
        if excel2xml.check_notna(row["Weight"]):
            resource.append(excel2xml.make_decimal_prop(":hasWeight", row["Weight"]))
        if excel2xml.check_notna(row["Birthday"]):
            birthday = excel2xml.find_date_in_string(row["Birthday"])
            if birthday:
                resource.append(excel2xml.make_date_prop(":hasBirthday", birthday))
        if excel2xml.check_notna(row["Neutered"]):
            resource.append(excel2xml.make_boolean_prop(":isNeutered", row["Neutered"]))

        # Append link Properties
        if excel2xml.check_notna(row["Link to Animal Friend ID"]):
            animal_friend_id = [x.strip() for x in row["Link to Animal Friend ID"].split(",")]
            resource.append(excel2xml.make_resptr_prop(":linkToAnimalFriendID", animal_friend_id))
        if excel2xml.check_notna(row["Link to Butler ID"]):
            butler_id = [x.strip() for x in row["Link to Butler ID"].split(",")]
            resource.append(excel2xml.make_resptr_prop(":linkToButlerID", butler_id))
        if excel2xml.check_notna(row["Link to Alice Character ID"]):
            alice_id = [x.strip() for x in row["Link to Alice Character ID"].split(",")]
            resource.append(excel2xml.make_resptr_prop(":linkToAliceCharacterID", alice_id))
        if excel2xml.check_notna(row["Link to Audio ID"]):
            audio_id = [x.strip() for x in row["Link to Audio ID"].split(",")]
            resource.append(excel2xml.make_resptr_prop(":linkToAudioID", audio_id))
        if excel2xml.check_notna(row["Link to Video ID"]):
            video_id = [x.strip() for x in row["Link to Video ID"].split(",")]
            resource.append(excel2xml.make_resptr_prop(":linkToVideoID", video_id))
        if excel2xml.check_notna(row["Link to Flyer ID"]):
            flyer_id = [x.strip() for x in row["Link to Flyer ID"].split(",")]
            resource.append(excel2xml.make_resptr_prop(":linkToFlyerID", flyer_id))

        # append the resource to the list
        all_resources.append(resource)
    # add all resources to the root
    root.extend(all_resources)

    excel2xml.write_xml(root,
                        "data/XML/import_animal_character.xml")
    return all_resources

if __name__ == "__main__":
    main()









