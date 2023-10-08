import datetime
from scraper.util import strfdelta, ask_question
from scraper.yt import get_songs_in_playlist
from scraper.threads import ThreadManager


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

    manager = ThreadManager(songs, 4)
    manager.start_download()

    print("Done")


