import pandas as pd
from dsp_tools.xmllib import Resource, create_list_from_input, find_dates_in_string


def main() -> list[Resource]:
    all_resources: list[Resource] = []

    # define dataframe
    book_df = pd.read_excel("data/spreadsheets/Book.xlsx", dtype="str")

    # iterate through rows of dataframe:
    for _, row in book_df.iterrows():
        # define variables
        dates_published = find_dates_in_string(row["Date Published"])
        book_chapter_ids = create_list_from_input(row["Book Chapter ID"], separator=",")
        book_edition_ids = create_list_from_input(row["Book Edition ID"], separator=",")
        video_ids = create_list_from_input(row["Video ID"], separator=",")
        cover_ids = create_list_from_input(row["Book Cover ID"], separator=",")
        authors_resource = create_list_from_input(input_value=row["Authorship Resource"], separator=",")

        # create resource, label and id
        resource = Resource.create_new(res_id=row["ID"], restype=":Book", label=row["Name"])

        # add properties to resource
        resource.add_simpletext("project-metadata:hasID", row["ID"])
        resource.add_simpletext(":hasName", row["Name"])
        resource.add_simpletext_multiple(":hasAuthorship", row["Authorship"])
        resource.add_richtext(":hasDescription", row["Description"])
        resource.add_richtext(prop_name=":hasDescriptionAlternative", value=row["Alternative Description"])
        resource.add_date_multiple(":hasDate", dates_published)
        resource.add_link_multiple(":linkToBookChapter", book_chapter_ids)
        resource.add_link_multiple(":linkToBookEdition", book_edition_ids)
        resource.add_link_multiple(":linkToVideo", video_ids)
        resource.add_link_multiple(":linkToBookCover", cover_ids)
        resource.add_simpletext("project-metadata:hasCopyrightResource", "DaSCH")
        resource.add_list("project-metadata:hasLicenseResource", "License", "LIC_002")
        resource.add_simpletext_multiple("project-metadata:hasAuthorshipResource", authors_resource)

        # append resource to list
        all_resources.append(resource)

    return all_resources


if __name__ == "__main__":
    main()
