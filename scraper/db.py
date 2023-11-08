from scraper import DATABASE_PATH, DATASET_DIR_PATH
import json
import uuid
import threading


DB_LOCK = threading.Lock()


def get_db():
    DB_LOCK.acquire()
    try:
        with open(DATABASE_PATH, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        db = {
            "songs": {},
        }
        with open(DATABASE_PATH, "w") as f:
            json.dump(db, f, indent=4)
        return db


def save_db(db):
    with open(DATABASE_PATH, "w") as f:
        json.dump(db, f, indent=4)
    DB_LOCK.release()


def add_song_to_db(id, title, artist, song_path, info_path, lyrics_path) -> str:
    """
    Add a song to the database and return its id as str
    """

    db = get_db()

    while id in db["songs"]:
        id = str(uuid.uuid4())

    db["songs"][id] = {
        "title": title,
        "artist": artist,
        "song_path": song_path,
        "info_json": info_path,
        "lyrics_path": lyrics_path,
    }
    save_db(db)

    return id


def list_songs():
    """
    List all the songs in the database
    """

    db = get_db()
    return db["songs"]


import os
import subprocess
import shlex


class Song:
    def __init__(self, song_id, song):
        self.id = song_id
        self.title = song["title"]
        self.artist = song["artist"]
        self.song_path = os.path.abspath(
            os.path.join(DATASET_DIR_PATH, str(self.id), song["song_path"])
        )
        self.info_json = os.path.abspath(
            os.path.join(DATASET_DIR_PATH, str(self.id), song["info_json"])
        )
        self.lyrics_path = os.path.abspath(
            os.path.join(DATASET_DIR_PATH, str(self.id), song["lyrics_path"])
        )

        cmd = f'ffprobe -i {self.song_path} -show_entries format=duration -v quiet -of csv="p=0"'
        cmd = shlex.split(cmd)
        proc = subprocess.run(
            cmd,
            text=True,
            capture_output=True,
        )

        self.duration = float(proc.stdout)

        self.index: int


def get_songs() -> list[Song]:
    db = get_db()
    songs = []
    for song_id, song in db["songs"].items():
        songs.append(Song(song_id, song))
    return songs
