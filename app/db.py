from app import DATABASE_PATH
import json
import uuid


def get_db():
    try:
        with open(DATABASE_PATH, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        db = {
            "songs": {},
        }
        save_db(db)
        return db


def save_db(db):
    with open(DATABASE_PATH, "w") as f:
        json.dump(db, f, indent=4)


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
