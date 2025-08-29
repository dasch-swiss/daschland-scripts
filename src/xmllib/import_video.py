import pandas as pd
from dsp_tools.xmllib import (
    LicenseRecommended,
    Resource,
    create_list_from_input,
)

from src.helpers.image_helper import (
    get_media_file_creation_time,
    get_media_file_size,
)


def main() -> list[Resource]:
    all_resources: list[Resource] = []

    # define dataframe
    video_df = pd.read_excel("data/spreadsheets/Video.xlsx", dtype="str")

    # iterate through rows of dataframe:
    for _, row in video_df.iterrows():
        # define variables
        video_path = f"{row['Directory']}{row['File Name']}"
        timestamp_value = get_media_file_creation_time(video_path)
        file_size_value = get_media_file_size(video_path)
        authors = create_list_from_input(input_value=row["Authorship"], separator=",")
        authors_resource = create_list_from_input(input_value=row["Authorship Resource"], separator=",")

        # create resource, label and id
        resource = Resource.create_new(
            res_id=row["ID"],
            restype=":Video",
            label=row["Label"],
        )

        # add file to resource
        resource.add_file(
            video_path,
            license=LicenseRecommended.DSP.PUBLIC_DOMAIN,
            copyright_holder=row["Copyright"],
            authorship=authors,
        )

        # add properties to resource
        resource.add_simpletext(":hasID", row["ID"])
        resource.add_time_optional(":hasTimeStamp", timestamp_value)
        resource.add_decimal_optional(":hasFileSize", file_size_value)
        resource.add_simpletext(":hasCopyrightResource", "DaSCH")
        resource.add_list(":hasLicenseResource", "License", "LIC_002")
        resource.add_simpletext_multiple(":hasAuthorshipResource", authors_resource)

        resource.add_simpletext(":hasFileName", row["File Name"])
        resource.add_richtext(":hasDescription", row["Description"])
        resource.add_textarea_optional(":hasCast", row["Cast"])

        # append resource to list
        all_resources.append(resource)

    return all_resources


if __name__ == "__main__":
    main()
