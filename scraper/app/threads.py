from app import CACHE_DIR_PATH, DATASET_DIR_PATH
from app.util import move_file
from app.yt import PlaylistSong, download_song
from app.db import add_song_to_db
import os
import threading
from blessings import Terminal


class Thread(threading.Thread):
    def __init__(self, manager, thread_id):
        self.manager = manager
        self.thread_id = thread_id
        super().__init__()

    def run(self):
        while True:
            song = self.manager.get_next_song()
            if song is None:
                self.output("No more songs to download")
                return
            self.add_song(song)

    def output(self, output):
        self.manager.outputs[self.thread_id - 1] = output
        self.manager.update_output()

    def add_song(self, song):
        song.index = self.manager.n_threads - song.index
        dl = download_song(song.url, self.output)
        if not dl:
            self.manager.print(f"[{song.index}/{self.manager.n_songs}] Failed to download song")
            return

        id = add_song_to_db(
            dl.id,
            dl.title,
            dl.artist,
            os.path.basename(dl.song_path),
            os.path.basename(dl.info_json_path),
            os.path.basename(dl.lyrics_path),
        )

        move_file(os.path.join(CACHE_DIR_PATH, dl.id), os.path.join(DATASET_DIR_PATH, id))

        self.manager.print(f"[{song.index}/{self.manager.n_songs}] - {dl.title}")


class ThreadManager:
    def __init__(self, songs: list[PlaylistSong], n_threads):
        self.songs = songs
        self.n_songs = len(songs)
        self.songs_lock = threading.Lock()
        self.n_threads = n_threads
        self.threads = []
        self.outputs = [""] * n_threads
        self.term = Terminal()

    def update_output(self):
        for i in range(self.n_threads):
            with self.term.location(0, self.term.height - i - 2):  # type: ignore
                print(self.outputs[i])

    def print(self, output):
        print()
        with self.term.location(0, self.term.height - self.n_threads - 2):
            print(output)
        self.update_output()

    def get_next_song(self):
        with self.songs_lock:
            if len(self.songs) == 0:
                return None
            return self.songs.pop()

    def start_download(self):
        for i in range(self.n_threads):
            print()

        for i in range(self.n_threads):
            thread = Thread(self, i + 1)
            thread.start()
            self.threads.append(thread)

        for thread in self.threads:
            thread.join()

