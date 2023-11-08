import argparse

parser = argparse.ArgumentParser(description="CLI for the model related commands")

command = parser.add_subparsers(dest="command", required=True)

command_create_dataset = command.add_parser(
    "create-dataset", help="Create a dataset from the songs in the database"
)

command_create_model = command.add_parser(
    "create-model", help="Create a model from the dataset"
)

command_predict = command.add_parser(
    "predict", help="Predict the song from the audio and lyrics"
)
command_predict.add_argument("audio", type=str, help="Path to the audio file")
command_predict.add_argument("lyrics", type=str, help="Part of the lyrics")


def main():
    args = parser.parse_args()
    if args.command == "create-dataset":
        from model.create_dataset import create_dataset

        create_dataset(args)

    elif args.command == "create-model":
        from model.create_model import create_model

        create_model(args)
    elif args.command == "predict":
        from model.predict import predict

        predict(args)
