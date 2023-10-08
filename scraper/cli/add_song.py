from scraper.threads import ThreadManager
from scraper.yt import PlaylistSong

def add_song_main(args):
    url = args.url
    songs = [PlaylistSong(None, url, None, 1)]
    manager = ThreadManager(songs, 1)
    manager.start_download()


