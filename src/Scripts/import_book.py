import pandas as pd
from dsp_tools import excel2xml
from src.Helper_Scripts import helper

def main():

    all_resources = []

    # define folder paths
    book_df = pd.read_excel("data/Spreadsheet_Data/Book.xlsx", dtype="str")

    # create the root element dsp-tools
    root = helper.make_root()

    # iterate through the rows of the old data from salsah:
    for _, row in book_df.iterrows():

        # create resource, label and id
        if not excel2xml.check_notna(row["ID"]):
            continue
        resource_id = row["ID"]
        resource_label = row["Name"]

        # create the `<resource>` tag
        resource = excel2xml.make_resource(
            label=resource_label,
            restype=":Book",
            id=resource_id)

        # Append Properties
        if excel2xml.check_notna(row["ID"]):
            resource.append(excel2xml.make_text_prop(":hasID", resource_id))
        if excel2xml.check_notna(row["Name"]):
            resource.append(excel2xml.make_text_prop(":hasName", row["Name"]))
        if excel2xml.check_notna(row["Author"]):
            resource.append(excel2xml.make_text_prop(":hasAuthor", row["Author"]))
        if excel2xml.check_notna(row["Description"]):
            resource.append(excel2xml.make_text_prop(":hasDescription", excel2xml.PropertyElement(row["Description"], encoding="xml")))
        if excel2xml.check_notna(row["Alternative Description"]):
            resource.append(excel2xml.make_text_prop(":hasAlternativeDescription",
                                                     excel2xml.PropertyElement(row["Alternative Description"], encoding="xml")))
        if excel2xml.check_notna(row["Date Published"]):
            date_published = excel2xml.find_date_in_string(row["Date Published"])
            if date_published:
                resource.append(excel2xml.make_date_prop(":hasDate", date_published))

        if excel2xml.check_notna(row["Book Chapter ID"]):
            book_chapter_ids = [x.strip() for x in row["Book Chapter ID"].split(",")]
            resource.append(excel2xml.make_resptr_prop(":linkToBookChapterID", book_chapter_ids))
        if excel2xml.check_notna(row["Audio ID"]):
            audio_ids = [x.strip() for x in row["Audio ID"].split(",")]
            resource.append(excel2xml.make_resptr_prop(":linkToAudioID", audio_ids))
        if excel2xml.check_notna(row["Video ID"]):
            video_ids = [x.strip() for x in row["Video ID"].split(",")]
            resource.append(excel2xml.make_resptr_prop(":linkToVideoID", video_ids))

        if excel2xml.check_notna(row["Copyright"]):
            resource.append(excel2xml.make_text_prop(":hasCopyright", row["Copyright"]))
        if excel2xml.check_notna(row["License List"]):
            resource.append(excel2xml.make_list_prop("License", ":hasLicenseList", row["License List"]))
        # append the resource to the list
        all_resources.append(resource)

    # add all resources to the root
    root.extend(all_resources)

    excel2xml.write_xml(root,
                        "data/XML/import_book.xml")
    return all_resources

if __name__ == "__main__":
    main()

