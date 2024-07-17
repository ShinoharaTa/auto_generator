import os
import random
import google.auth.transport.requests
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime
from PIL import Image
from modules.config import Config


class YouTubeUploader:
    def __init__(self, api_service_name='youtube', api_version='v3'):
        self.config = Config()
        self.config_detail = self.config.get_genre_config("cafe_jazz")
        secrets_path = self.config_detail["youtube"]["client_secrets_file"]
        self.client_secrets_file = os.path.join("config", secrets_path)
        self.scopes = ["https://www.googleapis.com/auth/youtube.upload"]
        self.api_service_name = api_service_name
        self.api_version = api_version
        self.service = self.get_authenticated_service()

    def get_authenticated_service(self):
        flow = InstalledAppFlow.from_client_secrets_file(
            self.client_secrets_file, self.scopes)
        credentials = flow.run_local_server(port=0)
        return build(self.api_service_name, self.api_version, credentials=credentials)

    def resize_image(self, image_path, max_size=2097152):
        with Image.open(image_path) as img:
            img_format = img.format
            img.thumbnail((1280, 720))
            img.save("temp_thumbnail.jpg", format=img_format,
                     optimize=True, quality=85)

        if os.path.getsize("temp_thumbnail.jpg") > max_size:
            raise MediaUploadSizeError(
                "Resized media larger than: %s" % max_size)

        return "temp_thumbnail.jpg"

    def read_description(self):
        description_file = self.config_detail["youtube"]["description_file"]
        file_path = os.path.join("config", description_file)
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def upload_video(self, file, thumbnail):
        description = self.read_description()
        title = self.config_detail["youtube"]["title"]
        tags = self.config_detail["youtube"]["tags"]
        sub_titles = self.config_detail["youtube"]["sub_title"]
        sub_title = random.choice(sub_titles)
        try:
            body = {
                'snippet': {
                    'title': f'{title} - {sub_title}',
                    'description': description,
                    'tags': tags,
                    'categoryId': '22',
                },
                'status': {
                    'privacyStatus': 'public',
                    "embeddable": False,
                    "selfDeclaredMadeForKids": False
                }
            }

            request = self.service.videos().insert(
                part="snippet,status",
                body=body,
                media_body=file
            )
            response = request.execute()

            video_id = response['id']
            thumbnail_path = self.resize_image(thumbnail)
            self.service.thumbnails().set(
                videoId=video_id,
                media_body=thumbnail_path
            ).execute()
            return video_id

        except HttpError as e:
            print(f"An HTTP error {e.resp.status} occurred: {e.content}")
            return None
