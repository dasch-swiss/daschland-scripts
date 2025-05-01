import pandas as pd
from dsp_tools.xmllib import VideoSegmentResource

from src.Helper_Scripts.cleaning_df_tools import create_list


def main() -> list[VideoSegmentResource]:
    all_segments: list[VideoSegmentResource] = []

    # define dataframe
    video_segment_df = pd.read_excel("data/spreadsheets/VideoSegment.xlsx")

    # iterate through rows of dataframe:
    for _, row in video_segment_df.iterrows():
        relates_to_ids = create_list(row["Relates To ID"])

        # create segment, label and id
        video_segment = VideoSegmentResource.create_new(
            res_id=row["ID"],
            label=row["Label"],
            segment_of=row["Video ID"],
            segment_start=row["Segment Start"],
            segment_end=row["Segment End"],
        )

        # add non-mandatory properties
        video_segment.add_comment_optional(row["Comment"])
        video_segment.add_description(row["Description"])
        video_segment.add_keyword(row["Keyword"])
        video_segment.add_relates_to_multiple(relates_to_ids)

        # append segment to list
        all_segments.append(video_segment)

    return all_segments


if __name__ == "__main__":
    main()
