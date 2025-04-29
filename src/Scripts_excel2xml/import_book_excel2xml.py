import pandas as pd
from dsp_tools import excel2xml
from src.Helper_Scripts import helper_excel2xml


def main():
    all_resources = []

    # create the root element dsp-tools
    root = helper.make_root()

    # define dataframe
    book_df = pd.read_excel("data/Spreadsheet_Data/Book.xlsx", dtype="str")

    # iterate through rows of dataframe:
    for _, row in book_df.iterrows():
        # define variables
        resource_id = row["ID"]
        resource_label = row["Name"]

        # create resource, label and id
        if not excel2xml.check_notna(row["ID"]):
            continue

        resource = excel2xml.make_resource(label=resource_label, restype=":Book", id=resource_id)

        # add properties to resource
        if excel2xml.check_notna(row["ID"]):
            resource.append(excel2xml.make_text_prop(":hasID", resource_id))
        if excel2xml.check_notna(row["Name"]):
            resource.append(excel2xml.make_text_prop(":hasName", row["Name"]))
        if excel2xml.check_notna(row["Authorship"]):
            authorship = [x.strip() for x in row["Authorship"].split(",")]
            resource.append(excel2xml.make_text_prop(":hasAuthorship", authorship))
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
        if excel2xml.check_notna(row["Date Published"]):
            date_published = excel2xml.find_date_in_string(row["Date Published"])
            if date_published:
                resource.append(excel2xml.make_date_prop(":hasDate", date_published))
        if excel2xml.check_notna(row["Book Chapter ID"]):
            book_chapter_ids = [x.strip() for x in row["Book Chapter ID"].split(",")]
            resource.append(excel2xml.make_resptr_prop(":linkToBookChapter", book_chapter_ids))
        if excel2xml.check_notna(row["Book Edition ID"]):
            book_edition_ids = [x.strip() for x in row["Book Edition ID"].split(",")]
            resource.append(excel2xml.make_resptr_prop(":linkToBookEdition", book_edition_ids))
        if excel2xml.check_notna(row["Video ID"]):
            video_ids = [x.strip() for x in row["Video ID"].split(",")]
            resource.append(excel2xml.make_resptr_prop(":linkToVideo", video_ids))
        if excel2xml.check_notna(row["Book Cover ID"]):
            cover_ids = [x.strip() for x in row["Book Cover ID"].split(",")]
            resource.append(excel2xml.make_resptr_prop(":linkToBookCover", cover_ids))

        # append the resource to the list
        all_resources.append(resource)

    # add all resources to the root
    root.extend(all_resources)

    # write root to xml file
    excel2xml.write_xml(root, "data/XML/import_book.xml")
    return all_resources


if __name__ == "__main__":
    main()
