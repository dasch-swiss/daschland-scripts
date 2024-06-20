import pandas as pd
from dsp_tools import excel2xml
from src.Helper_Scripts import helper
from src.Helper_Scripts.image_helper import get_image_creation_time
from src.Helper_Scripts.helper_mapping import make_cols_mapping_with_columns

def main():
    all_resources = []

    # define folder paths
    book_chapter_df = pd.read_excel("data/Spreadsheet_Data/BookChapter.xlsx", dtype="str")
    book_df = pd.read_excel("data/Spreadsheet_Data/Book.xlsx", dtype="str")
    mapping_book_name = make_cols_mapping_with_columns(df=book_df, value_column="Name")
    # create the root element dsp-tools
    root = helper.make_root()

    # create mapping

    # iterate through the rows of spreadsheet data:
    for _, row in book_chapter_df.iterrows():

        book = mapping_book_name[row["Book ID"]]

        # create resource, label and id
        if not excel2xml.check_notna(row["ID"]):
            continue
        resource_id = row["ID"]
        resource_label = f"{book} - {row["Name"]}"

        # create the `<resource>` tag
        resource = excel2xml.make_resource(
            label=resource_label,
            restype=":BookChapter",
            id=resource_id)

        # Append Properties
        if excel2xml.check_notna(row["ID"]):
            resource.append(excel2xml.make_text_prop(":hasID", resource_id))
        if excel2xml.check_notna(row["Name"]):
            resource.append(excel2xml.make_text_prop(":hasName", row["Name"]))
        if excel2xml.check_notna(row["Description"]):
            resource.append(excel2xml.make_text_prop(":hasDescription", excel2xml.PropertyElement(row["Description"], encoding="xml")))
        if excel2xml.check_notna(row["Chapter Number"]):
            resource.append(excel2xml.make_integer_prop(":hasChapterNumber", row["Chapter Number"]))
        if excel2xml.check_notna(row["URL"]):
            resource.append(excel2xml.make_uri_prop(":hasUrl", row["URL"]))

        # append link Properties
        if excel2xml.check_notna(row["Character ID"]):
            animal_id = [x.strip() for x in row["Character ID"].split(",")]
            resource.append(excel2xml.make_resptr_prop(":linkToCharacterID", animal_id))
        if excel2xml.check_notna(row["Location ID"]):
            alice_id = [x.strip() for x in row["Location ID"].split(",")]
            resource.append(excel2xml.make_resptr_prop(":linkToLocationID", alice_id))

        # append the resource to the list
        all_resources.append(resource)
    # add all resources to the root
    root.extend(all_resources)

    excel2xml.write_xml(root,
                        "data/XML/import_book_chapter.xml")
    return all_resources

if __name__ == "__main__":
    main()

