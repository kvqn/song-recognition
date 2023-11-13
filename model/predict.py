from tensorflow import keras
from model.create_model import (
    get_audio_embedding,
    get_text_embedding,
    combine_embeddings,
)
from typing import TypedDict
import pandas as pd
import os
from model import DATASET_DIR_PATH


def predict(args):
    audio = args.audio
    lyrics = args.lyrics

    lyrics_embedding = get_text_embedding(lyrics)
    audio_embedding = get_audio_embedding(audio)
    combined_embedding = combine_embeddings(lyrics_embedding, audio_embedding)

    model = keras.models.load_model("model.keras")
    print(model.predict(combined_embedding))


class Prediction(TypedDict):
    song: str
    artist: str
    confidence: float


def predict_from_embedding(audio_embedding, text_embedding):
    combined_embedding = combine_embeddings(text_embedding, audio_embedding)
    model = keras.models.load_model("model.keras")
    prediction = model.predict(combined_embedding)
    song_index = prediction.argmax()
    confidence = prediction.max()

    songs = pd.read_csv(os.path.join(DATASET_DIR_PATH, "dataset.csv"))
    song = songs.iloc[song_index]["title"]
    artst = songs.iloc[song_index]["artist"]

    return Prediction(song=song, artist=artst, confidence=confidence)
