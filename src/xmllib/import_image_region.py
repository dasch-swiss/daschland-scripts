import pandas as pd
from dsp_tools.xmllib import RegionResource

from src.folder_paths import RAW_FOLDER


def main() -> list[RegionResource]:
    all_resources: list[RegionResource] = []

    # define dataframe
    archive_df = pd.read_excel(RAW_FOLDER / "Region.xlsx")

    # iterate through rows of dataframe:
    for _, row in archive_df.iterrows():
        # create region, label and id
        region = RegionResource.create_new(
            res_id=row["ID"],
            label=row["Comment"],
            region_of=row["Image ID"],
        )

        # define variables
        point1 = (row["Geometry X1"], row["Geometry Y1"])
        point2 = (row["Geometry X2"], row["Geometry Y2"])

        # add properties to region
        region.add_rectangle(point1=point1, point2=point2, color=row["Color"], line_width=3)

        # add non-mandatory properties
        region.add_comment_optional(row["Comment"])

        # append region to list
        all_resources.append(region)

    return all_resources


if __name__ == "__main__":
    main()
