import argparse


_parser = argparse.ArgumentParser(description="Music Dataset CLI")
_subparsers = _parser.add_subparsers(
    help="Command for the CLI", dest="command", required=True
)

_list = _subparsers.add_parser("list", help="List all the available songs")

_search = _subparsers.add_parser("search", help="Search for a song")
_search.add_argument("query", help="Query to search for", type=str)

_add = _subparsers.add_parser("add", help="Add a playlist or a song")

_add_subparsers = _add.add_subparsers(
    help="Add song or playlist", dest="add_command", required=True
)

_add_song = _add_subparsers.add_parser("song", help="Add a song")
_add_song.add_argument("url", help="URL of the playlist or song", type=str)

_add_playlist = _add_subparsers.add_parser("playlist", help="Add a playlist")
_add_playlist.add_argument("url", help="URL of the playlist or song", type=str)

from .add_song import add_song_main
from .add_playlist import add_playlist_main
from .list import list_main
from .search import search_main


def main():
    args = _parser.parse_args()

    if args.command == "list":
        list_main(args)
    elif args.command == "search":
        search_main(args)
    elif args.command == "add" and args.add_command == "song":
        add_song_main(args)
    elif args.command == "add" and args.add_command == "playlist":
        add_playlist_main(args)
    else:
        print("Unknown command")
