import os
from dotenv import load_dotenv
import subprocess

load_dotenv()

CACHE_DIR_PATH = "cache"
DATASET_DIR_PATH = "database"
DATABASE_PATH = os.path.join(DATASET_DIR_PATH, "db.json")

if not os.path.exists(DATASET_DIR_PATH):
    os.mkdir(DATASET_DIR_PATH)

if not os.path.exists(CACHE_DIR_PATH):
    os.mkdir(CACHE_DIR_PATH)

YTDLP_PATH = os.getenv("YTDLP_PATH", "yt-dlp")


def check_youtube_dl_exist():
    return (
        subprocess.run(
            [YTDLP_PATH, "--version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        ).returncode
        == 0
    )
