import pandas as pd
from dsp_tools import excel2xml
from src.Helper_Scripts import helper_excel2xml


def main():
    all_resources = []

    # define json file path
    path_to_json = "daschland.json"

    # create the root element dsp-tools
    root = helper.make_root()

    # define dataframe
    book_df = pd.read_excel("data/Spreadsheet_Data/BookCover.xlsx", dtype="str")

    # create list mapping
    license_labels_to_names = excel2xml.create_json_list_mapping(
        path_to_json=path_to_json,
        list_name="License",
        language_label="en",
    )

    # iterate through rows of dataframe:
    for _, row in book_df.iterrows():
        # define variables
        resource_id = row["ID"]
        resource_label = row["Label"]
        uri = row["URI"]

        # create resource, label and id
        if not excel2xml.check_notna(row["ID"]):
            continue

        resource = excel2xml.make_resource(label=resource_label, restype=":BookCover", id=resource_id)

        # add file to resource
        resource.append(excel2xml.make_iiif_uri_prop(iiif_uri=uri))

        # add properties to resource
        if excel2xml.check_notna(row["ID"]):
            resource.append(excel2xml.make_text_prop(":hasID", resource_id))
        if excel2xml.check_notna(row["Description"]):
            resource.append(
                excel2xml.make_text_prop(
                    ":hasDescription",
                    excel2xml.PropertyElement(row["Description"], encoding="xml"),
                )
            )
        if excel2xml.check_notna(row["Copyright"]):
            resource.append(excel2xml.make_text_prop(":hasCopyright", row["Copyright"]))
        if excel2xml.check_notna(row["License List"]):
            license_name = license_labels_to_names.get(row["License List"])
            resource.append(excel2xml.make_list_prop("License", ":hasLicenseList", license_name))
        if excel2xml.check_notna(row["Source"]):
            resource.append(excel2xml.make_uri_prop(":hasUrl", row["Source"]))
        if excel2xml.check_notna(row["Authorship"]):
            authorship = [x.strip() for x in row["Authorship"].split(",")]
            resource.append(excel2xml.make_text_prop(":hasAuthorship", authorship))

        # append the resource to the list
        all_resources.append(resource)

    # add all resources to the root
    root.extend(all_resources)

    # write root to xml file
    excel2xml.write_xml(root, "data/XML/import_book_cover.xml")
    return all_resources


if __name__ == "__main__":
    main()
