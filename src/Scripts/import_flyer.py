import pandas as pd
from dsp_tools import excel2xml
from src.Helper_Scripts import helper

def main():
    all_resources = []

    # define folder paths
    originals_df = pd.read_excel("data/Spreadsheet_Data/Flyer.xlsx", dtype="str")

    # create the root element dsp-tools
    root = helper.make_root()

    # iterate through the rows of the old data from salsah:
    for _, row in originals_df.iterrows():

        # create resource, label and id
        if not excel2xml.check_notna(row["ID"]):
            continue
        resource_id = row["ID"]
        resource_label = row['File Name']

        # create the `<resource>` tag
        resource = excel2xml.make_resource(
            label=resource_label,
            restype=":Originals",
            id=resource_id)

        # create resource type "Image Human"
        originals_path = f"{row['Directory']}{row['File Name']}"
        resource.append(excel2xml.make_bitstream_prop(originals_path))

        if excel2xml.check_notna(row["ID"]):
            resource.append(excel2xml.make_text_prop(":hasID", resource_id))
        if excel2xml.check_notna(row["Description"]):
            resource.append(excel2xml.make_text_prop(":hasDescription", row["Description"]))

        # append the resource to the list
        all_resources.append(resource)
    # add all resources to the root
    root.extend(all_resources)

    excel2xml.write_xml(root,
                        "data/XML/import_flyer.xml")
    return all_resources

if __name__ == "__main__":
    main()