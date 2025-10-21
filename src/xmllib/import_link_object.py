import pandas as pd
from dsp_tools.xmllib import (
    LinkResource,
    create_list_from_input,
)

from src.folder_paths import RAW_FOLDER


def main() -> list[LinkResource]:
    all_link_resources: list[LinkResource] = []

    # define dataframe
    link_df = pd.read_excel(RAW_FOLDER / "LinkObject.xlsx", dtype="str")

    # iterate through rows of dataframe:
    for _, row in link_df.iterrows():
        # define variables
        links = create_list_from_input(input_value=row["Links"], separator=",")
        link_resource = LinkResource.create_new(res_id=row["ID"], label=row["Label"], link_to=links)

        link_resource = link_resource.add_comment(text=row["Text"], comment=row["Comment"])

        all_link_resources.append(link_resource)

    return all_link_resources


if __name__ == "__main__":
    main()
