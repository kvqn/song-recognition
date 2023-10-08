from app import DATABASE_PATH
from app.db import list_songs


def list_main(args):
    songs = list_songs()

    print(f"Currently storing {len(songs)} songs.")

    for id, song in songs.items():
        print(f"{id} - {song['title']}")
