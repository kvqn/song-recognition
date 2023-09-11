from app import DATASET_DIR_PATH
from app.util import check_youtube_dl_exist, move_file
from app.yt import InfoJson, download_song
from app.db import add_song
import os


def add_main(args):

    if not check_youtube_dl_exist():
        print("youtube-dl not found")
        return

    url = args.url

    dl = download_song(url)
    if not dl:
        print("Failed to download song")
        return

    title = InfoJson(dl.info_json_path).get_title()

    id = add_song(dl.id, title, os.path.basename(dl.song_path), os.path.basename(dl.info_json_path))

    os.mkdir(os.path.join(DATASET_DIR_PATH, id))
    move_file(dl.info_json_path, os.path.join(DATASET_DIR_PATH, id, "."))
    move_file(dl.song_path, os.path.join(DATASET_DIR_PATH, id, "."))

    print(f"Added song - {title}")



