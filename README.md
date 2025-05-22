# 🎬 YT-Short-Automator

## Overview

**YT-Short-Automator** is a Python-based tool designed to automate the creation of engaging, educational short-form videos (30–60 seconds long) from online articles. Just provide a link to an article, and the tool will:

1. Use **Gemini** (Google's generative AI) to summarize the article into a concise and compelling video script.
2. Convert the script to speech using a **Text-to-Speech (TTS)** engine.
3. Combine the audio with a video template and generate subtitles using **MoviePy**.
4. (Optional) Upload the finished video directly to your YouTube channel.

This project helps streamline content creation for educational, news, or infotainment-focused creators looking to capitalize on short-form video trends.

---

## Testing Instructions

Follow the steps below to generate your video:

### 1. Prepare `articles.txt`

Add your article(s) in the following format (one per line):


- `news` – This keyword indicates the type of content. Currently, only news sources are supported.
- `{title}` – The title you want to appear in the final video.
- `{link}` – The URL of the article you want to summarize.

**Example:**
news AI_Breakthrough https://example.com/news/ai-breakthrough

> ⚠️ Important:
> - Each article must be on a new line.
> - **Do not** include any extra blank lines in `articles.txt`.
> - Only use spaces to separate the elements.
### 2. Run Video.py
### 3. (Optional) Upload to YouTube
python upload.py
This uses the YouTube Data API to upload your video to your linked account.

## 📂 File Overview

| File           | Description                                                                 |
|----------------|-----------------------------------------------------------------------------|
| `Video.py`     | Main driver script. Combines script, TTS audio, subtitles, and template into a complete video. |
| `Summarizer.py`| Connects to the Gemini API and generates a short-form video script based on the article. |
| `Upload.py`    | Authenticates with your Google account and uploads the generated video to YouTube. |
| `articles.txt` | Input file for listing articles to summarize and convert.                   |

