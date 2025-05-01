import pandas as pd
from dsp_tools.xmllib import Resource

from src.Helper_Scripts.cleaning_df_tools import create_list


def main() -> list[Resource]:
    all_resources: list[Resource] = []

    # define dataframe
    location_df = pd.read_excel("data/spreadsheets/Location.xlsx", dtype="str")

    # iterate through rows of dataframe:
    for _, row in location_df.iterrows():
        # define variables
        resource_id = row["ID"]
        resource_label = row["Name"]
        descriptions = [
            row["Description EN"],
            row["Description DE"],
            row["Description FR"],
            row["Description IT"],
        ]
        descriptions = [description for description in descriptions if pd.notna(description)]
        image_ids = create_list(row["Image ID"])

        # create resource, label and id
        if row["Location Type List"] == "Real World":
            resource = Resource.create_new(res_id=resource_id, restype=":LocationRealWorld", label=resource_label)
        elif row["Location Type List"] == "Wonderland":
            resource = Resource.create_new(res_id=resource_id, restype=":LocationWonderland", label=resource_label)
        else:
            resource = Resource.create_new(res_id=resource_id, restype=":Location", label=resource_label)

        # add properties to resource
        resource.add_simpletext(":hasID", resource_id)
        resource.add_simpletext(":hasName", row["Name"])
        resource.add_richtext_multiple(prop_name=":hasDescription", values=descriptions)
        resource.add_link_multiple(":linkToImage", image_ids)
        resource.add_geoname_optional(":hasGeoname", row["Geoname ID"])

        # append resource to list
        all_resources.append(resource)

    return all_resources


if __name__ == "__main__":
    main()
