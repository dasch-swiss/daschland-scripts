import pandas as pd
from dsp_tools import excel2xml

from src.helpers import helper_excel2xml
from src.helpers.helper import make_cols_mapping_with_columns


def main():
    all_resources = []

    # define json file path
    path_to_json = "daschland.json"

    # create the root element dsp-tools
    root = helper_excel2xml.make_root()

    # define dataframes
    book_chapter_df = pd.read_excel("data/spreadsheets/BookChapter.xlsx", dtype="str")
    book_df = pd.read_excel("data/spreadsheets/Book.xlsx", dtype="str")

    # create list mapping
    keyword_labels_to_names = excel2xml.create_json_list_mapping(
        path_to_json=path_to_json,
        list_name="Keyword",
        language_label="en",
    )

    # create mapping
    mapping_book_name = make_cols_mapping_with_columns(df=book_df, value_column="Name")

    # iterate through rows of dataframe:
    for _, row in book_chapter_df.iterrows():
        # define variables
        book = mapping_book_name[row["Book ID"]]
        resource_id = row["ID"]
        resource_label = f"{book} - Chapter {row['Chapter Number']} - {row['Name']}"

        # create resource, label and id
        if not excel2xml.check_notna(row["ID"]):
            continue

        resource = excel2xml.make_resource(label=resource_label, restype=":BookChapter", id=resource_id)

        # add properties to resource
        if excel2xml.check_notna(row["ID"]):
            resource.append(excel2xml.make_text_prop(":hasID", resource_id))
        if excel2xml.check_notna(row["Name"]):
            resource.append(excel2xml.make_text_prop(":hasName", row["Name"]))
        if excel2xml.check_notna(row["Description"]):
            resource.append(
                excel2xml.make_text_prop(
                    ":hasDescription",
                    excel2xml.PropertyElement(row["Description"], encoding="xml", comment=row["Comment"]),
                )
            )
        if excel2xml.check_notna(row["Alternative Description"]):
            resource.append(
                excel2xml.make_text_prop(
                    ":hasDescriptionAlternative",
                    excel2xml.PropertyElement(
                        row["Alternative Description"],
                        permissions="prop-restricted",
                        encoding="xml",
                    ),
                )
            )
        if excel2xml.check_notna(row["Chapter Number"]):
            resource.append(excel2xml.make_integer_prop(":hasChapterNumber", row["Chapter Number"]))
        if excel2xml.check_notna(row["URL"]):
            resource.append(excel2xml.make_uri_prop(":hasUrl", row["URL"]))
        if excel2xml.check_notna(row["Full Text"]):
            resource.append(
                excel2xml.make_text_prop(
                    ":hasFullText",
                    excel2xml.PropertyElement(row["Full Text"], encoding="xml"),
                )
            )
        if excel2xml.check_notna(row["Keyword"]):
            keywords_names_raw = [x.strip() for x in row["Keyword"].split(",")]
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

        # append link Properties
        if excel2xml.check_notna(row["Audio ID"]):
            audio_ids = [x.strip() for x in row["Audio ID"].split(",")]
            resource.append(excel2xml.make_resptr_prop(":linkToAudio", audio_ids))
        if excel2xml.check_notna(row["Event ID"]):
            event_ids = [x.strip() for x in row["Event ID"].split(",")]
            resource.append(excel2xml.make_resptr_prop(":linkToEvent", event_ids))
        if excel2xml.check_notna(row["Location ID"]):
            location_ids = [x.strip() for x in row["Location ID"].split(",")]
            resource.append(excel2xml.make_resptr_prop(":linkToLocation", location_ids))

        # append the resource to the list
        all_resources.append(resource)

    # add all resources to the root
    root.extend(all_resources)

    # write root to xml file
    return all_resources


if __name__ == "__main__":
    main()
