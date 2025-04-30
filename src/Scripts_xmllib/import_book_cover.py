import pandas as pd
from dsp_tools.xmllib import (
    Resource,
    create_label_to_name_list_node_mapping,
    LicenseRecommended,
    create_list_from_string,
)


def main() -> list[Resource]:
    all_resources: list[Resource] = []

    # define json file path
    path_to_json = "daschland.json"

    # define dataframe
    book_df = pd.read_excel("data/Spreadsheet_Data/BookCover.xlsx", dtype="str")

    # create list mapping
    license_labels_to_names = create_label_to_name_list_node_mapping(
        project_json_path=path_to_json,
        list_name="License",
        language_of_label="en",
    )

    # iterate through rows of dataframe:
    for _, row in book_df.iterrows():
        # define variables
        license_name = license_labels_to_names.get(row["License List"])
        authors = create_list_from_string(string=row["Authorship"], separator=",")
        copyright_stripped = row["Copyright"].split("\n")
        copyright_stripped = [c.strip() for c in copyright_stripped if c.strip()]
        copyright_string = " ".join(copyright_stripped)
        # create resource, label and id
        resource = Resource.create_new(
            res_id=row["ID"],
            restype=":BookCover",
            label=row["Label"],
        )

        # add properties to resource
        resource.add_iiif_uri(
            row["URI"],
            license=LicenseRecommended.DSP.PUBLIC_DOMAIN,
            copyright_holder=copyright_string,
            authorship=authors,
        )
        resource.add_simpletext(":hasID", row["ID"])
        resource.add_richtext(":hasDescription", row["Description"])
        resource.add_simpletext(":hasCopyright", row["Copyright"])
        resource.add_list_optional(":hasLicenseList", "License", license_name)
        resource.add_uri(":hasUrl", row["Source"])
        resource.add_simpletext_multiple(":hasAuthorship", row["Authorship"])

        # append resource to list
        all_resources.append(resource)

    return all_resources


if __name__ == "__main__":
    main()
