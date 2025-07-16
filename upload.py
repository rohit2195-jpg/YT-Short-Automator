import os
import google_auth_httplib2
import google_auth_oauthlib
import googleapiclient.discovery
import googleapiclient.errors
import googleapiclient.http

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
TOKEN_FILE = 'token.json'


def authenticate_youtube():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    if os.path.exists(TOKEN_FILE):
        os.remove(TOKEN_FILE)

    # Load client secrets file, put the path of your file
    client_secrets_file = "client.json"

    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, SCOPES)
    credentials = flow.run_local_server()

    youtube = googleapiclient.discovery.build(
        "youtube", "v3", credentials=credentials)

    return youtube


def upload_video(youtube, media_file, title):
    request_body = {
        "snippet": {
            "categoryId": "22",
            "title": title,
            "description": "Subscribe for more breaking news",
            "tags": ["shorts", "news", "viral", "breaking", "important"]
        },
        "status": {
            "privacyStatus": "public"
        }
    }



    request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=googleapiclient.http.MediaFileUpload(media_file, chunksize=-1, resumable=True)
    )

    response = None

    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Upload {int(status.progress() * 100)}%")

        print(f"Video uploaded with ID: {response['id']}")


if __name__ == "__main__":
    youtube = authenticate_youtube()
    path = os.path.join(".", "finishedVideos")
    for file in os.listdir(path):
        print(file)
        upload_video(youtube, os.path.join(path, file), file[0:20])