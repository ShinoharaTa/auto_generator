import yaml
import os

class Config:

    config_path = "./config/"
    def __init__(self, main_config_file=f'{config_path}config.yaml'):
        with open(main_config_file, 'r') as file:
            self.main_config = yaml.safe_load(file)

    def get_config(self):
        return self.main_config

    def get_sounds_path(self):
        resource_base = self.main_config['resources']
        sounds_dir = self.main_config['sounds_dir']
        return os.path.join(resource_base, sounds_dir)

    def get_images_path(self):
        resource_base = self.main_config['resources']
        images_dir = self.main_config['images_dir']
        return os.path.join(resource_base, images_dir)

    def get_videos_path(self, genre):
        resource_base = self.main_config['resources']
        return os.path.join(resource_base, "videos",  genre)

    def get_genres(self):
        return self.main_config['genres']

    def get_genre_config(self, genre):
        with open(f'{self.config_path}{genre}.yaml', 'r') as file:
            return yaml.safe_load(file)

    def __repr__(self):
        return yaml.dump(self.main_config, default_flow_style=False)
