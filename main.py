import json
import  os
from edit import cut_video, convert_seconds, set_frame
import time


# trim option configuration...
videoTrimOptions = json.load(open('VideoTrimOptions.json', 'r'))

if not os.path.exists(videoTrimOptions['output_folder']):
    os.mkdir(videoTrimOptions["output_folder"])

#start time and end time in seconds...
trim_starts_from = convert_seconds(videoTrimOptions['Trim_Starts_From'])
trim_ends_with = convert_seconds(videoTrimOptions['Trim_Ends_With'])


cut_video(videoTrimOptions["Video_Path"], trim_starts_from, trim_ends_with)

# video_files = os.listdir(videoTrimOptions['output_folder'])
# video_files.sort()
# print(video_files)
# for i in range(3,0,-1):
#     print(f"framming starts in {i}", end="\r")
#     time.sleep(1)

# part=1
# for vid_file in video_files:
#     output_video_path = f"{videoTrimOptions['output_folder']}/{vid_file.split('.')[0]}_with_frame.mp4"
#     input_video_path = f"{videoTrimOptions['output_folder']}/{vid_file}"
#     set_frame(input_video_path, output_video_path, f"Part {part}")
#     part+=1
