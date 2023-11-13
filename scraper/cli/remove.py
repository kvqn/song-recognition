import json
from scraper import DATABASE_PATH, DATASET_DIR_PATH
import shutil
import os


def remove(args):
    song_id = args.id

    with open(DATABASE_PATH, "r") as f:
        db = json.load(f)

    if song_id not in db["songs"]:
        print("Song not found")
        return

    shutil.rmtree(os.path.join(DATASET_DIR_PATH, str(song_id)))
    song_name = db["songs"][song_id]["title"]
    artist = db["songs"][song_id]["artist"]
    del db["songs"][song_id]
    with open(DATABASE_PATH, "w") as f:
        json.dump(db, f, indent=4)

    print(f"Removed {song_name} by {artist}")
