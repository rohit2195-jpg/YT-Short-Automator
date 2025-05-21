from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, vfx, AudioFileClip
import os

# Make sure to initialize variables
video = VideoFileClip("templates/m5.mp4")
subtitles = []
audio = AudioFileClip("audioClips/clothes.mp3")

words = ["This", "is", "a", "list", "of", "words", "that", "will", "be", "used", "for", "subtitles"]
average_word_duration = 0.5  # Adjust to your need
total_duration = audio.duration
curr_sec = 0
screen_width = 300
title = "my_video"

# Loop through the words
for i in range(0, len(words), 6):
    if (i < 6):
        subtitle_str = words[i] + " " + words[i+1] + " " + words[i+2]
    elif (i > len(words) - 6):
        subtitle_str = words[i-2] + " " + words[i-1] + " " + words[i]
    else:
        subtitle_str = words[i-2] + " " + words[i-1] + " " + words[i] + " " + words[i+1] + " " + words[i+2] + " " + words[i+3]

    txt_clip = TextClip(
        text=subtitle_str,
        color='white',
        method="label",
        size=(screen_width, 75),
        stroke_color='white',
        stroke_width=1,
    )


    txt_clip = txt_clip.set_position("center").set_start(curr_sec).set_end(curr_sec + average_word_duration * 6)

    subtitles.append(txt_clip)
    curr_sec += average_word_duration * 6

# Final video composite
final_video = CompositeVideoClip([video] + subtitles).subclip(0, total_duration)
final_video.audio = audio
final_video = final_video.fx(vfx.speedx, 1.25)

# Save the video
save_path = os.path.join("finishedVideos", title)
final_video.write_videofile(save_path + ".mp4", codec="libx264", audio_codec="aac")
