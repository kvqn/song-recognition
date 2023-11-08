import argparse

parser = argparse.ArgumentParser(description="CLI for the model related commands")

command = parser.add_subparsers(dest="command", required=True)

command_create_dataset = command.add_parser(
    "create-dataset", help="Create a dataset from the songs in the database"
)


def main():
    args = parser.parse_args()
    if args.command == "create-dataset":
        from model.create_dataset import create_dataset

        create_dataset(args)
