import json
from edit import cut_video, convert_seconds


# trim option configuration...
videoTrimOptions = json.load(open('VideoTrimOptions.json', 'r'))


#start time and end time in seconds...
trim_starts_from = convert_seconds(videoTrimOptions['Trim_Starts_From'])
trim_ends_with = convert_seconds(videoTrimOptions['Trim_Ends_With'])


cut_video(videoTrimOptions["Video_Path"], videoTrimOptions["output_folder"], trim_starts_from, trim_ends_with)
