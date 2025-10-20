import pandas as pd
from dsp_tools import excel2xml

from src.folder_paths import SPREADSHEETS_FOLDER
from src.helpers import helper_excel2xml


def main():
    all_segments = []

    # create the root element dsp-tools
    root = helper_excel2xml.make_root()

    # define dataframe
    video_segment_df = pd.read_excel(SPREADSHEETS_FOLDER / "VideoSegment.xlsx")

    # iterate through rows of dataframe:
    for _, row in video_segment_df.iterrows():
        # define variables
        video_segment_id = row["ID"]
        video_label = row["Label"]

        # create segment, label and id
        if not excel2xml.check_notna(row["ID"]):
            continue

        segment = excel2xml.make_video_segment(video_label, video_segment_id)

        # add link to resource
        segment.append(excel2xml.make_isSegmentOf_prop(row["Video ID"]))
        segment.append(
            excel2xml.make_hasSegmentBounds_prop(segment_start=row["Segment Start"], segment_end=row["Segment End"])
        )

        # add properties to resource
        if excel2xml.check_notna(row["Title"]):
            segment.append(excel2xml.make_hasTitle_prop(row["Title"]))
        if excel2xml.check_notna(row["Comment"]):
            segment.append(excel2xml.make_hasComment_prop(row["Comment"]))
        if excel2xml.check_notna(row["Description"]):
            segment.append(excel2xml.make_hasDescription_prop(row["Description"]))
        if excel2xml.check_notna(row["Keyword"]):
            segment.append(excel2xml.make_hasKeyword_prop(row["Keyword"]))
        if excel2xml.check_notna(row["Relates To ID"]):
            segment.append(excel2xml.make_relatesTo_prop(row["Relates To ID"]))

        # append the segment to the list
        all_segments.append(segment)

    # add all resources to the root
    root.extend(all_segments)

    # write root to xml file
    return all_segments


if __name__ == "__main__":
    main()
