import os
import json
from pathlib import Path

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request


SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

BASE_DIR = Path(__file__).parent
CLIENT_SECRET_FILE = BASE_DIR / "client_secret.json"
TOKEN_FILE = BASE_DIR / "youtube_token.json"

VIDEOS_DIR = BASE_DIR / "output" / "videos"
PACKAGES_DIR = BASE_DIR / "output" / "upload_packages"
THUMBNAILS_DIR = BASE_DIR / "output" / "thumbnails"


def get_youtube_service():
    creds = None

    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CLIENT_SECRET_FILE),
                SCOPES
            )
            creds = flow.run_local_server(port=0)

        TOKEN_FILE.write_text(creds.to_json())

    return build("youtube", "v3", credentials=creds)


def get_latest_file(folder, extension):
    files = list(folder.glob(f"*{extension}"))
    if not files:
        raise FileNotFoundError(f"No {extension} files found in {folder}")
    return max(files, key=os.path.getmtime)


def upload_latest_short():
    youtube = get_youtube_service()

    video_file = get_latest_file(VIDEOS_DIR, ".mp4")
    metadata_file = get_latest_file(PACKAGES_DIR, ".json")

    with open(metadata_file, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    title = metadata.get("title", "AI60Seconds Short")
    description = metadata.get("description", "")
    tags = metadata.get("tags", ["AI", "Shorts", "AI60Seconds"])

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": "27"
        },
        "status": {
            "privacyStatus": "private",
            "selfDeclaredMadeForKids": False
        }
    }

    media = MediaFileUpload(
        str(video_file),
        chunksize=-1,
        resumable=True,
        mimetype="video/mp4"
    )

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )

    print(f"Uploading video: {video_file.name}")
    response = request.execute()

    video_id = response["id"]
    video_url = f"https://www.youtube.com/watch?v={video_id}"

    print("Upload complete!")
    print(video_url)

    return video_url


if __name__ == "__main__":
    upload_latest_short()