import os
import random
from datetime import datetime
from moviepy.editor import *
from modules.config import Config


class VideoCreator:
    def __init__(self, genre, sounds, images, video_duration=60*60):
        self.genre_name = genre
        self.music_files = sounds
        self.image_files = images
        self.video_duration = video_duration
        self.config = Config()

    def get_files(self, dir_path, extensions):
        return [os.path.join(dir_path, f) for f in os.listdir(dir_path) if f.endswith(extensions)]

    def select_random_files(self, files, count=3):
        return random.sample(files, count)

    def create_video(self):
        selected_music_files = self.select_random_files(self.music_files)
        selected_image_files = self.select_random_files(self.image_files)

        video_clips = []
        current_duration = 0

        while current_duration < self.video_duration:
            for music_file, image_file in zip(selected_music_files, selected_image_files):
                if current_duration >= self.video_duration:
                    break
                music_clip = AudioFileClip(os.path.join(
                    self.config.get_sounds_path(), music_file))
                music_duration = music_clip.duration

                img_clip = ImageClip(os.path.join(
                    self.config.get_images_path(), image_file)).set_duration(music_duration)
                img_clip = img_clip.set_audio(music_clip)
                img_clip = img_clip.crossfadein(3).crossfadeout(3)

                video_clips.append(img_clip)

                current_duration += music_duration

        final_video = concatenate_videoclips(
            video_clips, method="compose", padding=-3)

        output_filename = datetime.now().strftime("%Y%m%d%H%M%S") + ".mp4"
        output_dir = self.config.get_videos_path(self.genre_name)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        output_filepath = os.path.join(output_dir, output_filename)

        final_video.write_videofile(
            output_filepath, codec='libx264', audio_codec='aac', fps=24)
