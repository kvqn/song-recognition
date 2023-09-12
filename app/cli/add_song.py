from app import CACHE_DIR_PATH, DATASET_DIR_PATH
from app.util import move_file
from app.yt import download_song
from app.db import add_song_to_db
import os


def add_song_main(args):
    url = args.url
    add_song(url)


def add_song(url, index=1, outof=1):
    dl = download_song(url)
    if not dl:
        print("Failed to download song")
        return

    id = add_song_to_db(
        dl.id,
        dl.title,
        dl.artist,
        os.path.basename(dl.song_path),
        os.path.basename(dl.info_json_path),
        os.path.basename(dl.lyrics_path),
    )

    move_file(os.path.join(CACHE_DIR_PATH, dl.id), os.path.join(DATASET_DIR_PATH, id))

    if index == outof == 1:
        print(f"Added song - {dl.title}")
    else:
        print(f"Added song {index}/{outof} - {dl.title}")
