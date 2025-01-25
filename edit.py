import cv2
import numpy as np
from moviepy import VideoFileClip

# Load the video with moviepy
input_video_path = 'output_clips\clip_1.mp4'
clip = VideoFileClip(input_video_path)

# Get video properties
fps = clip.fps
frame_width = clip.w
frame_height = clip.h

# Define the target resolution (9:16 aspect ratio)
target_width = 1080
target_height = 1920

# Create the video writer to save the output (using OpenCV)
output_video_path = 'output_video.mp4'
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_video_path, fourcc, fps, (target_width, target_height))

# Text settings
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1.5
font_color = (255, 255, 255)  # White
font_thickness = 2
text = 'Part 1'

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
    text_y = frame_with_black_bg.shape[0] - 20  # Position at the bottom
    cv2.putText(frame_with_black_bg, text, (text_x, text_y), font, font_scale, font_color, font_thickness)

    # Write the processed frame to the output video
    out.write(frame_with_black_bg)

# Release the video writer
out.release()

# Now handle the audio using moviepy and combine it with the processed video
video = VideoFileClip(input_video_path)
audio = video.audio

# Load the output video (without audio) and set its audio
final_video = VideoFileClip(output_video_path)
final_video = final_video.with_audio(audio)

# Write the final video with audio to the output file
final_video.write_videofile("final_output_with_audio.mp4", codec="libx264", audio_codec="aac")

# Close everything
video.close()
final_video.close()
