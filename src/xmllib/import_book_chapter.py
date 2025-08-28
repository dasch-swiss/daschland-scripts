import pandas as pd
from dsp_tools.xmllib import ListLookup, Resource, create_list_from_input

from src.helpers.helper import make_cols_mapping_with_columns


def main() -> list[Resource]:
    all_resources: list[Resource] = []

    # define json file path
    path_to_json = "daschland.json"

    # define dataframes
    book_chapter_df = pd.read_excel("data/spreadsheets/BookChapter.xlsx", dtype="str")
    book_df = pd.read_excel("data/spreadsheets/Book.xlsx", dtype="str")

    # create list mapping
    list_lookup = ListLookup.create_new(
        project_json_path=path_to_json,
        language_of_label="en",
        default_ontology="daschland",
    )

    # create mapping
    mapping_book_name = make_cols_mapping_with_columns(df=book_df, value_column="Name")

    # iterate through rows of dataframe:
    for _, row in book_chapter_df.iterrows():
        # define variables
        keywords_names_raw = create_list_from_input(row["Keyword"], separator=",")
        keyword_names = [
            list_lookup.get_node_via_list_name(list_name="Keyword", node_label=x) for x in keywords_names_raw
        ]
        keyword_names = sorted(keyword_names)

        book = mapping_book_name[row["Book ID"]]
        audio_ids = create_list_from_input(row["Audio ID"], separator=",")
        event_ids = create_list_from_input(row["Event ID"], separator=",")
        location_ids = create_list_from_input(row["Location ID"], separator=",")
        authors_resource = create_list_from_input(input_value=row["Authorship Resource"], separator=",")

        # create resource, label and id
        resource = Resource.create_new(
            res_id=row["ID"],
            restype=":BookChapter",
            label=f"{book} - Chapter {row['Chapter Number']} - {row['Name']}"
            if pd.notna(row["Chapter Number"])
            else f"{book} - {row['Name']}",
        )

        # add properties to resource
        resource.add_simpletext(":hasID", row["ID"])
        resource.add_simpletext(":hasName", row["Name"])
        resource.add_richtext(prop_name=":hasDescription", value=row["Description"], comment=row["Comment"])
        resource.add_richtext(prop_name=":hasDescriptionAlternative", value=row["Alternative Description"])
        resource.add_integer_optional(":hasChapterNumber", row["Chapter Number"])
        resource.add_uri_optional(":hasUrl", row["URL"])
        resource.add_richtext(":hasFullText", row["Full Text"])
        resource.add_list_multiple(":hasKeywordList", "Keyword", keyword_names)
        resource.add_link_multiple(":linkToAudio", audio_ids)
        resource.add_link_multiple(":linkToEvent", event_ids)
        resource.add_link_multiple(":linkToLocation", location_ids)
        resource.add_simpletext(":hasCopyrightResource", "DaSCH")
        resource.add_list(":hasLicenseResource", "License", "LIC_002")
        resource.add_simpletext_multiple(":hasAuthorshipResource", authors_resource)
        # append resource to list
        all_resources.append(resource)

    return all_resources


if __name__ == "__main__":
    main()
