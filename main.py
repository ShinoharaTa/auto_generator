from modules.video_creator import VideoCreator
from modules.config import Config

main_config = Config()
print(main_config.get_config())
sub_config = main_config.get_genre_config("cafe_jazz")
print(sub_config)

sounds = sub_config["sounds"]
images = sub_config["images"]
genre = "cafe_jazz"
video_duration = 2*60

print(sounds)

video_creator = VideoCreator(genre, sounds, images, video_duration)
video_creator.create_video()
