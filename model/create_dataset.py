import json
from scraper.db import get_songs, Song
import pandas as pd
import os
from model import DATASET_DIR_PATH
import subprocess
import shlex
import shutil


def _process_song(song: Song):
    audio_output_dir = os.path.join(DATASET_DIR_PATH, "audio", str(song.index))
    os.makedirs(audio_output_dir, exist_ok=True)
    for clip_index, start in enumerate(range(0, int(song.duration) - 5, 5)):
        # Get song segment
        subprocess.run(
            [
                "ffmpeg",
                "-ss",
                str(start),
                "-t",
                "5",
                "-v",
                "0",
                "-i",
                song.song_path,
                os.path.join(audio_output_dir, f"{clip_index}.wav"),
            ]
        )

    lyrics_output_dir = os.path.join(DATASET_DIR_PATH, "lyrics")
    os.makedirs(lyrics_output_dir, exist_ok=True)
    shutil.copyfile(
        song.lyrics_path, os.path.join(lyrics_output_dir, f"{song.index}.txt")
    )


def create_dataset(args):
    if os.path.exists(DATASET_DIR_PATH):
        resp = input("Dataset already exists. Delete and continue? [y/N] ").lower()
        if resp in ["y", "yes"]:
            subprocess.run(["rm", "-rf", DATASET_DIR_PATH])
        else:
            return

    os.makedirs(DATASET_DIR_PATH, exist_ok=True)

    songs = get_songs()

    df = pd.DataFrame(columns=["index", "title", "artist", "duration"])

    for i, song in enumerate(songs):
        song.index = i
        df.loc[i] = [i, song.title, song.artist, song.duration]
        _process_song(song)

    df.to_csv(os.path.join(DATASET_DIR_PATH, "dataset.csv"), index=False)
