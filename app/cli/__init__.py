import argparse


_parser = argparse.ArgumentParser(description='Music Dataset CLI')
_subparsers = _parser.add_subparsers(help='Command for the CLI', dest='command', required=True)

_list = _subparsers.add_parser('list', help='List all the available songs')

_search = _subparsers.add_parser('search', help='Search for a song')
_search.add_argument('query', help='Query to search for', type=str)

_add = _subparsers.add_parser('add', help='Add a playlist or a song')
_add.add_argument('url', help='URL of the playlist or song', type=str)

from .add import add_main
from .list import list_main
from .search import search_main

def main():

    args = _parser.parse_args()

    match args.command:
        case 'list':
            list_main(args)
        case 'search':
            search_main(args)
        case 'add':
            add_main(args)

