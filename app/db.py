import sqlite3


class Database:
    def __init__(self, database: str):
        self._conn = sqlite3.connect(database)
        self._cursor = self._conn.cursor()
        self._cursor.execute(
            """create table if not exists songs
            (id integer primary key autoincrement,
             title text not null,
             artist text,
             duration integer,
             path text not null,
             lyrics_path text not null,
             album_art_path text
             )"""
        )

    def list_songs(self):
        """List all the available songs"""
        self._cursor.execute("SELECT * FROM songs")
        return self._cursor.fetchall()

    def add_song(self, title, artist, duration, path, lyrics_path, album_art_path):
        """Add a song to the database"""
        self._cursor.execute(
            "INSERT INTO songs (title, artist, duration, path, lyrics_path, album_art_path) VALUES (?, ?, ?, ?, ?, ?)",
            (title, artist, duration, path, lyrics_path, album_art_path),
        )
        self._conn.commit()
