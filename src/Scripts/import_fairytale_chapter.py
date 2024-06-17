import pandas as pd
from dsp_tools import excel2xml
from src.Helper_Scripts import helper
from src.Helper_Scripts.image_helper import get_image_creation_time
from src.Helper_Scripts.helper_mapping import make_cols_mapping_with_columns

def main():
    all_resources = []

    # define folder paths
    fairytale_chapter_df = pd.read_excel("data/Spreadsheet_Data/FairytaleChapter.xlsx", dtype="str")
    fairytale_df = pd.read_excel("data/Spreadsheet_Data/Fairytale.xlsx", dtype="str")
    mapping_fairytale_name = make_cols_mapping_with_columns(df=fairytale_df, value_column="Name")
    # create the root element dsp-tools
    root = helper.make_root()

    # create mapping

    # iterate through the rows of the old data from salsah:
    for _, row in fairytale_chapter_df.iterrows():


        fairytale = mapping_fairytale_name[row["Part of Fairytale ID"]]

        # create resource, label and id
        if not excel2xml.check_notna(row["ID"]):
            continue
        resource_id = row["ID"]
        resource_label = f"{fairytale} - {row["Name"]}"

        # create the `<resource>` tag
        resource = excel2xml.make_resource(
            label=resource_label,
            restype=":FairytaleChapter",
            id=resource_id)

        # create resource type "Image Human"
        image_path = f"{row['Image Directory']}{row['File Name']}"
        resource.append(excel2xml.make_bitstream_prop(image_path))

        if excel2xml.check_notna(row["ID"]):
            resource.append(excel2xml.make_text_prop(":hasID", resource_id))
        if excel2xml.check_notna(row["Name"]):
            resource.append(excel2xml.make_text_prop(":hasName", row["Name"]))
        if excel2xml.check_notna(row["Description"]):
            resource.append(excel2xml.make_text_prop(":hasDescription", row["Description"]))

        #append link Properties
        if excel2xml.check_notna(row["Part of Fairytale ID"]):
            resource.append(excel2xml.make_resptr_prop(":isPartOfFairytaleID", row["Part of Fairytale ID"]))
        if excel2xml.check_notna(row["Chapter Number"]):
            resource.append(excel2xml.make_integer_prop(":hasChapterNumber", row["Chapter Number"]))
        if excel2xml.check_notna(row["Link to Animal Character ID"]):
            resource.append(excel2xml.make_resptr_prop(":linkToAnimalCharacterID", row["Link to Animal Character ID"]))
        if excel2xml.check_notna(row["Link to Alice Character ID"]):
            resource.append(excel2xml.make_resptr_prop(":linkToAnimalCharacterID", row["Link to Alice Character ID"]))

        # append the resource to the list
        all_resources.append(resource)
    # add all resources to the root
    root.extend(all_resources)

    excel2xml.write_xml(root,
                        "data/XML/import_fairytale_chapter.xml")
    return all_resources

if __name__ == "__main__":
    main()

