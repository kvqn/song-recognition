import torch
import pandas as pd
import os
from model import DATASET_DIR_PATH
import tensorflow as tf
from tensorflow import keras
import numpy as np
import pickle

_audio_embedding_model = torch.hub.load("harritaylor/torchvggish", "vggish")
_audio_embedding_model.eval()

try:
    with open("audio_embedding.pkl", "rb") as f:
        _audio_embedding_saved = pickle.load(f)
except FileNotFoundError:
    _audio_embedding_saved = {}


def get_audio_embedding(audio_path) -> np.ndarray:
    if audio_path in _audio_embedding_saved:
        return _audio_embedding_saved[audio_path]

    ret = (
        _audio_embedding_model.forward(audio_path)
        .reshape(1, -1)
        .detach()
        .apply_(lambda x: x / 256)
    )
    ret = ret.detach().numpy()
    ret = ret[0]
    _audio_embedding_saved[audio_path] = ret
    with open("audio_embedding.pkl", "wb") as f:
        pickle.dump(_audio_embedding_saved, f)
    return ret


from towhee import AutoPipes

_text_embedding_model = AutoPipes.pipeline("sentence_embedding")


def get_text_embedding(text) -> np.ndarray:
    return _text_embedding_model(text).get()[0]


def create_model(args):
    df = pd.read_csv(os.path.join(DATASET_DIR_PATH, "dataset.csv"))
    print(df)

    X = []
    Y = []

    n_songs = len(df)

    for _, song in df.iterrows():
        song_clips_dir = os.path.join(
            DATASET_DIR_PATH, "audio_train", str(song["index"])
        )
        song_clips = os.listdir(song_clips_dir)
        song_clips = [os.path.join(song_clips_dir, clip) for clip in song_clips]
        song_clips_embeddings = [get_audio_embedding(clip) for clip in song_clips]

        lyrics_path = os.path.join(DATASET_DIR_PATH, "lyrics", f"{song['index']}.txt")
        with open(lyrics_path) as f:
            lyrics = f.read()
        words = lyrics.split()
        lyrics_segments = [
            " ".join(words[i : i + 10]) for i in range(0, len(words), 10)
        ]
        # print(lyrics_segments)
        lyrics_segments_embeddings = [
            get_text_embedding(text) for text in lyrics_segments
        ]

        x = []
        for text_emb in lyrics_segments_embeddings:
            for song_emb in song_clips_embeddings:
                _x = np.concatenate((text_emb, song_emb)).reshape(1, -1)
                _x = np.expand_dims(_x, axis=2)
                x.append(_x)

        _y = np.zeros((1, n_songs))
        _y[0, song["index"]] = 1
        y = [_y] * len(x)

        Y.extend(y)
        X.extend(x)
    # X is just text embedding then audio embedding
    # Y is just a zero array with one 1 at the index of the song

    print(len(X))
    print(len(Y))
    print(X[0].shape)
    print(Y[0].shape)

    # X = np.expand_dims(X, axis=2)

    Z = tf.data.Dataset.from_tensor_slices((X, Y))

    X_val = []
    Y_val = []

    for _, song in df.iterrows():
        song_clips_dir = os.path.join(
            DATASET_DIR_PATH, "audio_test", str(song["index"])
        )
        song_clips = os.listdir(song_clips_dir)
        song_clips = [os.path.join(song_clips_dir, clip) for clip in song_clips]
        song_clips_embeddings = [get_audio_embedding(clip) for clip in song_clips]

        lyrics_path = os.path.join(DATASET_DIR_PATH, "lyrics", f"{song['index']}.txt")
        with open(lyrics_path) as f:
            lyrics = f.read()
        words = lyrics.split()
        lyrics_segments = [
            " ".join(words[i : i + 10]) for i in range(5, len(words), 10)
        ]
        # print(lyrics_segments)
        lyrics_segments_embeddings = [
            get_text_embedding(text) for text in lyrics_segments
        ]

        x = []
        for text_emb in lyrics_segments_embeddings:
            for song_emb in song_clips_embeddings:
                _x = np.concatenate((text_emb, song_emb)).reshape(1, -1)
                _x = np.expand_dims(_x, axis=2)
                x.append(_x)

        _y = np.zeros((1, n_songs))
        _y[0, song["index"]] = 1
        y = [_y] * len(x)

        Y_val.extend(y)
        X_val.extend(x)

    Z_val = tf.data.Dataset.from_tensor_slices((X_val, Y_val))

    model = keras.Sequential()
    # model.add(keras.layers.Input(shape=(1, 5 * 128 + 384)))
    model.add(
        keras.layers.Conv1D(
            8, 4, use_bias=True, activation="relu", input_shape=(5 * 128 + 384, 1)
        )
    )
    model.add(
        keras.layers.Flatten(),
    )
    # model.add(keras.layers.MaxPool1D(2))
    model.add(keras.layers.Dense(n_songs, activation="softmax"))

    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )

    model.summary()

    model.fit(Z, epochs=10, validation_data=Z_val)

    model.save("model.keras")
