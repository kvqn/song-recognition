import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_PATH = "db.json"
CACHE_DIR_PATH = "cache"
DATASET_DIR_PATH = "dataset"

if not os.path.exists(DATASET_DIR_PATH):
    os.mkdir(DATASET_DIR_PATH)

if not os.path.exists(CACHE_DIR_PATH):
    os.mkdir(CACHE_DIR_PATH)

YTDLP_PATH = os.getenv("YTDLP_PATH", "yt-dlp")
