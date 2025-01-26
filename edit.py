import cv2
import numpy as np
from moviepy import VideoFileClip
import os
import time
import threading

def convert_seconds(data):
    second = 0
    second += data['hour']*3600
    second += data['minute']*60
    second += data['second']
    return second



def cut_video(input_video_path, output_folder, trim_starts_from, trim_ends_with, clip_duration=60):
    # Load the video file
    video = VideoFileClip(input_video_path)
    
    # Get the video duration (in seconds)
    video_duration = video.duration
    
    # Calculate how many full clips there will be
    num_clips = int((video_duration - trim_starts_from - (video_duration-trim_ends_with)) // clip_duration)

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
        time.sleep(2)

        # starting a thread to add frame
        clip_with_frame_path = f"{output_folder}/clip_{i+1}_with_frame.mp4"
        threading.Thread(target=set_frame, args=(output_file, clip_with_frame_path, f"Part {i+1}")).start()
    
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
        time.sleep(2)

        # start a thread to add frame
        clip_with_frame_path = f"{output_folder}/clip_{num_clips+1}_with_frame.mp4"
        threading.Thread(target=set_frame, args=(output_file, clip_with_frame_path, f"Part {num_clips+1}")).start()

    print(f"Video has been cut into {num_clips + 1} clips.")



def set_frame(input_video_path, output_video_path, text):
    # Load the video with moviepy
    # input_video_path = 'output_clips\clip_1.mp4'
    clip = VideoFileClip(input_video_path)

    # Get video properties
    fps = clip.fps
    frame_width = clip.w
    frame_height = clip.h

    # Define the target resolution (9:16 aspect ratio)
    target_width = 1080
    target_height = 1920

    # Create the video writer to save the output (using OpenCV)
    # output_video_path = 'output_video.mp4'
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (target_width, target_height))

    # Text settings
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 2
    font_color = (255, 255, 255)  # White
    font_thickness = 4
    # text = 'Part 1'

    # Process the video frames
    for frame in clip.iter_frames(fps=fps, dtype="uint8"):
        # Resize the video while maintaining its aspect ratio
        aspect_ratio = frame_width / frame_height
        new_width = target_width
        new_height = int(new_width / aspect_ratio)

        if new_height > target_height:
            new_height = target_height
            new_width = int(new_height * aspect_ratio)

        # Resize frame to fit 9:16 aspect ratio
        frame_resized = cv2.resize(frame, (new_width, new_height))

        # Create a black background with 9:16 aspect ratio (1080x1920)
        frame_with_black_bg = np.zeros((target_height, target_width, 3), dtype=np.uint8)

        # Calculate the position to center the resized video on the black background
        x_offset = (target_width - new_width) // 2
        y_offset = (target_height - new_height) // 2

        # Place the resized video on the black background
        frame_with_black_bg[y_offset:y_offset + new_height, x_offset:x_offset + new_width] = frame_resized

        # Add the text "Part 1" at the bottom
        text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]
        text_x = (frame_with_black_bg.shape[1] - text_size[0]) // 2  # Center the text
        text_y = frame_with_black_bg.shape[0]//4  # Position at the top
        cv2.putText(frame_with_black_bg, text, (text_x, text_y), font, font_scale, font_color, font_thickness)

        # Write the processed frame to the output video
        out.write(frame_with_black_bg)

    # Release the video writer
    out.release()
    time.sleep(2)
    # Now handle the audio using moviepy and combine it with the processed video
    video = VideoFileClip(input_video_path)
    audio = video.audio

    # Load the output video (without audio) and set its audio
    final_video = VideoFileClip(output_video_path)
    final_video = final_video.with_audio(audio)

    # Write the final video with audio to the output file
    output_video_path = f"{output_video_path.split('/')[0]}/final_{output_video_path.split('/')[1]}"
    final_video.write_videofile(output_video_path, codec="libx264", audio_codec="aac")

    # Close everything
    video.close()
    final_video.close()

    #delete previous videos
    os.remove(input_video_path)
    os.remove(output_video_path.split('final_')[0] + output_video_path.split('final_')[1])

