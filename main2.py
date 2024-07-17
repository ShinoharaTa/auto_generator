import os
import time
import random
from modules.youtube_uploader import YouTubeUploader
from modules.config import Config

uploader = YouTubeUploader()
config = Config()
genre_name = "cafe_jazz"
main_config = config.get_config()
genre_config = config.get_genre_config(genre_name)
resource_path = main_config["resources"]
videos_dir = os.path.join(resource_path, "videos", genre_name)
thumbnails_dir = os.path.join(resource_path, "thumbnails")
uploaded_dir = os.path.join(resource_path, "uploaded", genre_name)

video_files = [os.path.join(videos_dir, f)
               for f in os.listdir(videos_dir) if f.endswith('.mp4')]
thumbnail_file = random.choice(genre_config["thumbnails"])

for video_file in video_files:
    video_id = uploader.upload_video(
        video_file, os.path.join(thumbnails_dir, thumbnail_file))

    if video_id:
        uploaded_path = os.path.join(
            uploaded_dir, os.path.basename(video_file))
        os.rename(video_file, uploaded_path)
        print(
            f"Uploaded {video_file} to {uploaded_path} with video ID {video_id}")

    time.sleep(10)
