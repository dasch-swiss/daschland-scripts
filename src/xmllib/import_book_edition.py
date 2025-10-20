import pandas as pd
from dsp_tools.xmllib import (
    LicenseRecommended,
    Resource,
    create_list_from_input,
    find_dates_in_string,
)

from src.folder_paths import SPREADSHEETS_FOLDER
from src.helpers.image_helper import get_media_file_creation_time


def main() -> list[Resource]:
    all_resources: list[Resource] = []

    # define dataframe
    book_df = pd.read_excel(SPREADSHEETS_FOLDER / "BookEdition.xlsx", dtype="str")

    # iterate through rows of dataframe:
    for _, row in book_df.iterrows():
        # define variables
        book_path = f"{row['Directory']}{row['File Name']}"
        timestamp_value = get_media_file_creation_time(book_path)
        authors = create_list_from_input(input_value=row["Authorship"], separator=",")
        authors_resource = create_list_from_input(input_value=row["Authorship Resource"], separator=",")
        date_published = find_dates_in_string(row["Date Published"])

        # create resource, label and id
        resource = Resource.create_new(res_id=row["ID"], restype=":BookEdition", label=row["File Name"])

        # add file to resource
        resource.add_file(
            filename=book_path,
            license=LicenseRecommended.DSP.PUBLIC_DOMAIN,
            copyright_holder=row["Copyright"],
            authorship=authors,
        )

        # add properties to resource
        resource.add_simpletext("project-metadata:hasID", row["ID"])
        resource.add_simpletext("project-metadata:hasFileName", row["File Name"])
        resource.add_richtext(":hasDescription", row["Description"])
        resource.add_time_optional("project-metadata:hasTimeStamp", timestamp_value)
        resource.add_simpletext("project-metadata:hasCopyrightResource", "DaSCH")
        resource.add_list("project-metadata:hasLicenseResource", "License", "LIC_002")
        resource.add_simpletext_multiple("project-metadata:hasAuthorshipResource", authors_resource)
        resource.add_date_multiple(":hasDate", date_published)

        # append resource to list
        all_resources.append(resource)

    return all_resources


if __name__ == "__main__":
    main()
