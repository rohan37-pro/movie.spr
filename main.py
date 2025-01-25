import platform
import os
from moviepy import VideoFileClip


def cut_video(input_video_path, output_folder, trim_starts_from, trim_ends_with, clip_duration=60):
    # Load the video file
    video = VideoFileClip(input_video_path)
    
    # Get the video duration (in seconds)
    video_duration = video.duration
    
    # Calculate how many full clips there will be
    num_clips = int((video_duration - trim_starts_from - (video_duration-trim_ends_with)) // clip_duration)
    print(num_clips)
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Loop through each full 1-minute clip and save it
    for i in range(num_clips):
        start_time = i * clip_duration  # Starting time of the clip (in seconds)
        end_time = (i + 1) * clip_duration  # Ending time of the clip (in seconds)
        start_time += trim_starts_from
        end_time += trim_starts_from
        # Make the subclip
        subclip = video.subclipped(start_time, end_time)
        
        # Define the output path for the current clip
        output_file = f"{output_folder}/clip_{i + 1}.mp4"
        
        # Write the subclip to the file (including audio)
        subclip.write_videofile(output_file, audio=True)
    
    # Save the remaining part of the video (if any) as the last clip
    remaining_time = trim_ends_with - ((num_clips * clip_duration) + trim_starts_from)
    if remaining_time > 0:
        start_time = (num_clips * clip_duration) + trim_starts_from  # Start from where the last clip ended
        end_time = start_time + remaining_time
        output_file = f"{output_folder}/clip_{num_clips + 1}.mp4"
        
        # Make the subclip for the remaining time
        subclip = video.subclipped(start_time, end_time)

        
        # Write the remaining subclip to the file
        subclip.write_videofile(output_file, audio=True)

    print(f"Video has been cut into {num_clips + 1} clips.")

# Example usage
input_video_path = "Jeene Laga Hoon_360.mp4"  # Replace with your input video file path
output_folder = "output_clips"  # Folder where clips will be saved

#start time and end time in seconds...
trim_starts_from = 37
trim_ends_with = 192

cut_video(input_video_path, output_folder, trim_starts_from, trim_ends_with)
