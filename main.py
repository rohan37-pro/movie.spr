from moviepy import VideoFileClip
import os

def cut_video(input_video_path, output_folder, clip_duration=60):
    # Load the video file
    video = VideoFileClip(input_video_path)
    
    # Get the video duration (in seconds)
    video_duration = video.duration
    
    # Calculate how many full clips there will be
    num_clips = int(video_duration // clip_duration)
    
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Loop through each full 1-minute clip and save it
    for i in range(num_clips):
        start_time = i * clip_duration  # Starting time of the clip (in seconds)
        end_time = (i + 1) * clip_duration  # Ending time of the clip (in seconds)

        # Make the subclip
        subclip = video.subclipped(start_time, end_time)
        
        # Define the output path for the current clip
        output_file = f"{output_folder}/clip_{i + 1}.mp4"
        
        # Write the subclip to the file (including audio)
        subclip.write_videofile(output_file, audio=True)
    
    # Save the remaining part of the video (if any) as the last clip
    remaining_time = video_duration - (num_clips * clip_duration)
    if remaining_time > 0:
        start_time = num_clips * clip_duration  # Start from where the last clip ended
        output_file = f"{output_folder}/clip_{num_clips + 1}.mp4"
        
        # Make the subclip for the remaining time
        subclip = video.subclipped(start_time, video_duration)
        
        # Write the remaining subclip to the file
        subclip.write_videofile(output_file, audio=True)

    print(f"Video has been cut into {num_clips + 1} clips.")

# Example usage
input_video_path = "M4rc0.24.br.HIN.1080p.sdm0v13sp01nt.mp4.mkv"  # Replace with your input video file path
output_folder = "output_clips"  # Folder where clips will be saved

cut_video(input_video_path, output_folder)
