import pandas as pd
from dsp_tools.xmllib import AudioSegmentResource


def main():
    all_segments = []

    # define dataframe
    audio_segment_df = pd.read_excel("data/Spreadsheet_data/AudioSegment.xlsx")

    # iterate through rows of dataframe:
    for _, row in audio_segment_df.iterrows():
        # create resource, label and id
        audio_segment = AudioSegmentResource.create_new(
            res_id=row["ID"],
            label=row["Label"],
            segment_of=row["Audio ID"],
            segment_start=row["Segment Start"],
            segment_end=row["Segment End"],
        )

        # add non-mandatory properties
        audio_segment.add_comment_optional(row["Comment"])
        audio_segment.add_description(row["Description"])
        audio_segment.add_keyword(row["Keyword"])
        audio_segment.add_relates_to_optional(row["Relates To ID"])

        # append resource to list
        all_segments.append(audio_segment)

    return all_segments


if __name__ == "__main__":
    main()
