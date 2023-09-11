

from app import DATABASE_PATH
from app.db import Database


def list_main(args):
    print("List all the available songs")

    db = Database(DATABASE_PATH)
    print(db.list_songs())



