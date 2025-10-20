import json

import pandas as pd
from dsp_tools import excel2xml

from src.folder_paths import SPREADSHEETS_FOLDER
from src.helpers import helper_excel2xml


def main():
    all_resources = []

    # create the root element dsp-tools
    root = helper_excel2xml.make_root()

    # define dataframe
    archive_df = pd.read_excel(SPREADSHEETS_FOLDER / "Region.xlsx")

    # iterate through rows of dataframe:
    for _, row in archive_df.iterrows():
        # define variables
        region_id = row["ID"]
        region_label = row["Comment"]
        color = row["Color"]
        x1 = row["Geometry X1"]
        y1 = row["Geometry Y1"]
        x2 = row["Geometry X2"]
        y2 = row["Geometry Y2"]
        geometry = {
            "status": "active",
            "type": "rectangle",
            "lineColor": color,
            "lineWidth": 5,
            "points": [{"x": x1, "y": y1}, {"x": x2, "y": y2}],
        }
        JSON_string = json.dumps(geometry)

        # create region, label and id
        if not excel2xml.check_notna(row["ID"]):
            continue

        region = excel2xml.make_region(label=region_label, id=region_id)

        # add properties to resource
        if excel2xml.check_notna(row["Color"]):
            region.append(excel2xml.make_color_prop("hasColor", row["Color"]))
        if excel2xml.check_notna(row["Image ID"]):
            region.append(excel2xml.make_resptr_prop("isRegionOf", row["Image ID"]))
        if excel2xml.check_notna(row["Geometry X1"]):
            region.append(excel2xml.make_geometry_prop("hasGeometry", JSON_string))
        if excel2xml.check_notna(row["Comment"]):
            region.append(
                excel2xml.make_text_prop("hasComment", excel2xml.PropertyElement(value=row["Comment"], encoding="xml"))
            )

        # append the region to the list
        all_resources.append(region)

    # add all resources to the root
    root.extend(all_resources)

    # write root to xml file
    return all_resources


if __name__ == "__main__":
    main()
