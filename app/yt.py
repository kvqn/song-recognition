import subprocess
from . import YTDLP_PATH
import uuid
import json
from app import CACHE_DIR_PATH
import os

class DownloadedSong:
    def __init__(self, id, song_path, info_json_path):
        self.id = id
        self.song_path = song_path
        self.info_json_path = info_json_path


def download_song(url) -> DownloadedSong | None:
    """
    Download a song from YouTube
    """

    id = str(uuid.uuid4())
    cache_dir = os.path.join(CACHE_DIR_PATH, id)
    os.mkdir(cache_dir)

    proc = subprocess.run([YTDLP_PATH, "--progress", "-xq", "-o", os.path.join(cache_dir, "%(title)s.%(ext)s"), "--restrict-filenames", "--write-info-json", url])
    if proc.returncode != 0:
        return None

    info_json_path = None
    song_path = None
    for file in os.listdir(cache_dir):
        if file.endswith(".info.json"):
            info_json_path = os.path.join(cache_dir, file)
        else:
            song_path = os.path.join(cache_dir, file)

    if info_json_path is None or song_path is None:
        return None

    return DownloadedSong(id, song_path, info_json_path)


class InfoJson:
    def __init__(self, info_json_path):
        self.info_json_path = info_json_path
        with open(info_json_path) as f:
            self.info = json.load(f)

    def get_title(self):
        return self.info["title"]

