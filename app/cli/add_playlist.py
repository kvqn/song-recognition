import datetime
from app.cli.add_song import add_song
from app.util import strfdelta, ask_question

from app.yt import get_songs_in_playlist


def add_playlist_main(args):
    url = args.url
    songs = get_songs_in_playlist(url)

    print(f"Found {len(songs)} songs in playlist")

    for song in songs:
        duration = strfdelta(datetime.timedelta(seconds=song.duration))
        print(f"{duration} - {song.title}")

    print("Check the songs above and confirm to add them to the dataset")

    if not ask_question("Confirm? (y/n): "):
        print("Aborting")
        return

    for i, song in enumerate(songs):
        add_song(song.url, i + 1, len(songs))

    print("Done")
