
from moviepy.editor import *
import requests
from gtts import gTTS
import os
from pydub import AudioSegment
import random
from summarizer import summarizer






with open("articles.txt", "r") as f:
    lines = f.readlines()

    for line in lines:
        # number of videos len(lines)

        title = "yaya"
        summary = ""


        if ("reddit" in line.split(" ")[0]):
            post_url = line.split(" ")[2].strip() + ".json"
            response = requests.get(post_url)
            if (response.status_code == 200):
                data = response.json()
                title = data[0]["data"]["children"][0]["data"]["title"]
                summary = data[0]["data"]["children"][0]["data"]["selftext"]

        elif ("news" in line.split(" ")[0]):
            summary = summarizer(line.split(" ")[2].strip())
            title  = line.split(" ")[1]
            summary = summary.split('\n')[0]

        print(summary)
        tts = gTTS(text=summary, lang="en")
        save_path = os.path.join("audioClips", title)
        tts.save(save_path+".mp3")

        audio = AudioFileClip(save_path+".mp3")
        total_duration = audio.duration

        words = summary.split(" ")
        average_word_duration = total_duration / len(words)

        index = 0
        random_index = random.randint(0, len(os.listdir("templates")) -1)
        chosen_vid = ""
        for video in os.listdir("templates/"):
            if (index == random_index):
                chosen_vid = video
                break
            index += 1
        chosen_vid = os.path.join("templates", chosen_vid)
        video = VideoFileClip(chosen_vid)
        video = video.without_audio()

        subtitles = []
        curr_sec = 0

        for i in range(0, len(words), 6):

            if (i < 6):
                list = words[i] + " " + words[i+1] + " " + words[i+2]
            elif (i > len(words) - 6):
                list = words[i-2] + " " + words[i - 1] + " " + words[i]
            else:
                list = words[i-2] + " " + words[i-1] + " " + words[i] +" "+ words[i+1] + " " + words[i+2] + " " + words[i+3]

            screen_width = 300
            txt_clip = TextClip(
                list,
                color='white',  # Text color
                method="label",  # Ensure the text wraps correctly
                size=(screen_width, 75),  # Dynamically adjust height based on the text
                stroke_color='white',  # Add a stroke to make text stand out
                stroke_width=1,  # Make the stroke width thick enough for visibility
            )


            txt_clip = txt_clip.on_color(color=(0, 0, 0), col_opacity=0.7)  # Black background with opacity
            txt_clip = txt_clip.set_opacity(1)

            txt_clip = txt_clip.set_position("center").set_start(curr_sec).set_end(curr_sec + average_word_duration*6)

            subtitles.append(txt_clip)
            curr_sec += average_word_duration*6


        final_video = CompositeVideoClip([video] + subtitles).subclip(0, total_duration)
        final_video.audio = audio
        final_video = final_video.fx(vfx.speedx, 1.25)
        save_path = os.path.join("finishedVideos", title)
        final_video.write_videofile(save_path+".mp4", audio_codec="aac")





















