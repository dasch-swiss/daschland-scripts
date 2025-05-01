import pandas as pd
from dsp_tools.xmllib import Permissions, Resource, find_date_in_string

from src.helpers.cleaning_df_tools import create_list


def main() -> list[Resource]:
    all_resources: list[Resource] = []

    # define dataframe
    book_df = pd.read_excel("data/spreadsheets/Book.xlsx", dtype="str")

    # iterate through rows of dataframe:
    for _, row in book_df.iterrows():
        # define variables
        date_published = find_date_in_string(row["Date Published"])
        file_permissions = Permissions.RESTRICTED
        book_chapter_ids = create_list(row["Book Chapter ID"])
        book_edition_ids = create_list(row["Book Edition ID"])
        video_ids = create_list(row["Video ID"])
        cover_ids = create_list(row["Book Cover ID"])

        # create resource, label and id
        resource = Resource.create_new(res_id=row["ID"], restype=":Book", label=row["Name"])

        # add properties to resource
        resource.add_simpletext(":hasID", row["ID"])
        resource.add_simpletext(":hasName", row["Name"])
        resource.add_simpletext_multiple(":hasAuthorship", row["Authorship"])
        resource.add_richtext(":hasDescription", row["Description"])
        resource.add_richtext(
            prop_name=":hasDescriptionAlternative",
            value=row["Alternative Description"],
            permissions=file_permissions,
        )
        resource.add_date_optional(":hasDate", date_published)
        resource.add_link_multiple(":linkToBookChapter", book_chapter_ids)
        resource.add_link_multiple(":linkToBookEdition", book_edition_ids)
        resource.add_link_multiple(":linkToVideo", video_ids)
        resource.add_link_multiple(":linkToBookCover", cover_ids)

        # append resource to list
        all_resources.append(resource)

    return all_resources


if __name__ == "__main__":
    main()
