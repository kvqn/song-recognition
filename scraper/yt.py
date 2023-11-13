import subprocess

from . import YTDLP_PATH
import uuid
import json
from scraper import CACHE_DIR_PATH
import os
import azapi


class DownloadedSong:
    def __init__(self, id, title, artist, song_path, info_json_path, lyrics_path):
        self.id = id
        self.title = title
        self.artist = artist
        self.song_path = song_path
        self.info_json_path = info_json_path
        self.lyrics_path = lyrics_path


def download_song(url, output_func=print) -> DownloadedSong | None:
    """
    Download a song from YouTube
    """

    id = str(uuid.uuid4())
    cache_dir = os.path.join(CACHE_DIR_PATH, id)
    os.mkdir(cache_dir)

    output_func("Downloading song...")

    proc = subprocess.run(
        [
            YTDLP_PATH,
            # "--progress",
            "-xq",
            "-o",
            os.path.join(cache_dir, "%(title)s.%(ext)s"),
            "--restrict-filenames",
            "--write-info-json",
            url,
        ]
    )
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

    info = InfoJson(info_json_path)
    title = info.get_title()

    output_func("Downloading lyrics...")

    az = azapi.AZlyrics("google", accuracy=0.3)
    az.title = title
    az.getLyrics()
    title = az.title
    artist = az.artist

    lyrics_path = os.path.join(cache_dir, "lyrics.txt")
    if len(az.lyrics.strip()) == 0:
        output_func("No lyrics found. Skipping")
        return None

    with open(lyrics_path, "w") as f:
        f.write(az.lyrics)

    return DownloadedSong(id, title, artist, song_path, info_json_path, lyrics_path)


class InfoJson:
    def __init__(self, info_json_path):
        self.info_json_path = info_json_path
        with open(info_json_path) as f:
            self.info = json.load(f)

    def get_title(self):
        return self.info["title"]


class PlaylistSong:
    def __init__(self, title, url, duration, index):
        self.title = title
        self.url = url
        self.duration = duration
        self.index = index


def get_songs_in_playlist(url):
    proc = subprocess.run(
        [YTDLP_PATH, "--flat-playlist", "--dump-single-json", url], capture_output=True
    )
    if proc.returncode != 0:
        raise Exception("Failed to get playlist")

    playlist = json.loads(proc.stdout)

    songs = []
    bad = 0
    prev_index = 0
    for song in playlist["entries"]:
        title = song["title"]
        url = song["url"]
        duration = song["duration"]
        if not title or not url or not duration:
            bad += 1
            continue
        prev_index += 1
        songs.append(PlaylistSong(title, url, duration, prev_index))

    print(f"{bad} bad songs")
    return songs
