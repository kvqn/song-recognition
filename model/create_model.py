import pandas as pd
import os
from model import DATASET_DIR_PATH
import tensorflow as tf
from tensorflow import keras
import numpy as np
import pickle
from pyAudioAnalysis import audioBasicIO, ShortTermFeatures

# _audio_embedding_model = torch.hub.load("harritaylor/torchvggish", "vggish")
# _audio_embedding_model.eval()

try:
    with open("audio_embedding.pkl", "rb") as f:
        _audio_embedding_saved = pickle.load(f)
except FileNotFoundError:
    _audio_embedding_saved = {}

try:
    with open("song_train_embeddings.pkl", "rb") as f:
        _song_train_embeddings = pickle.load(f)
except FileNotFoundError:
    _song_train_embeddings = {}

try:
    with open("song_test_embeddings.pkl", "rb") as f:
        _song_test_embeddings = pickle.load(f)
except FileNotFoundError:
    _song_test_embeddings = {}


def get_audio_embedding(audio_path) -> np.ndarray:
    if audio_path in _audio_embedding_saved:
        return _audio_embedding_saved[audio_path]

    sampling_rate, signal = audioBasicIO.read_audio_file(audio_path)
    signal = audioBasicIO.stereo_to_mono(signal)

    short_term_features, _ = ShortTermFeatures.feature_extraction(
        signal, sampling_rate, 0.050 * sampling_rate, 0.025 * sampling_rate
    )

    ret = short_term_features.reshape(1, -1)
    ret = ret[0]

    _audio_embedding_saved[audio_path] = ret
    with open("audio_embedding.pkl", "wb") as f:
        pickle.dump(_audio_embedding_saved, f)
    return ret


from towhee import AutoPipes

_text_embedding_model = AutoPipes.pipeline("sentence_embedding")


def get_text_embedding(text) -> np.ndarray:
    return _text_embedding_model(text).get()[0]


def combine_embeddings(text_embedding, audio_embedding):
    ret = np.concatenate((text_embedding, audio_embedding)).reshape(1, -1)
    ret = np.expand_dims(ret, axis=2)
    return ret


def create_model(args):
    df = pd.read_csv(os.path.join(DATASET_DIR_PATH, "dataset.csv"))
    print(df)

    n_songs = len(df)

    model = keras.Sequential()
    # model.add(keras.layers.Input(shape=(1, 5 * 128 + 384)))
    model.add(keras.layers.InputLayer(input_shape=(13916, 1)))
    # model.add(keras.layers.Activation("sigmoid"))
    # model.add(keras.layers.Conv1D(16, 4, use_bias=True, activation="relu"))
    # model.add(keras.layers.MaxPooling1D(8, 4))
    model.add(keras.layers.Flatten())
    # model.add(keras.layers.Dense(200, activation="relu"))
    # model.add(keras.layers.MaxPool1D(2))
    model.add(keras.layers.Dense(n_songs, activation="softmax"))

    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )

    model.summary()

    X = []
    Y = []

    for _, song in df.iterrows():
        if song["index"] in _song_train_embeddings:
            X.extend(_song_train_embeddings[song["index"]]["x"])
            Y.extend(_song_train_embeddings[song["index"]]["y"])
            continue
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
        # for text_emb in lyrics_segments_embeddings:
        #     for song_emb in song_clips_embeddings:
        #         x.append(combine_embeddings(text_emb, song_emb))

        for text_emb in lyrics_segments_embeddings:
            x.append(combine_embeddings(text_emb, np.zeros((13532,))))

        for song_emb in song_clips_embeddings:
            x.append(combine_embeddings(np.zeros((384,)), song_emb))

        _y = np.zeros((1, n_songs))
        _y[0, song["index"]] = 1
        y = [_y] * len(x)

        _song_train_embeddings[song["index"]] = {"x": x, "y": y}
        with open("song_train_embeddings.pkl", "wb") as f:
            pickle.dump(_song_train_embeddings, f)

        Y.extend(y)
        X.extend(x)
    # X is just text embedding then audio embedding
    # Y is just a zero array with one 1 at the index of the song

    # print(len(X))
    # print(len(Y))
    # print(X[0].shape)
    # print(Y[0].shape)

    # X = np.expand_dims(X, axis=2)

    Z = tf.data.Dataset.from_tensor_slices((X, Y))

    X_val = []
    Y_val = []

    for _, song in df.iterrows():
        if song["index"] in _song_test_embeddings:
            X_val.extend(_song_test_embeddings[song["index"]]["x"])
            Y_val.extend(_song_test_embeddings[song["index"]]["y"])
            continue
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
                x.append(combine_embeddings(text_emb, song_emb))

        _y = np.zeros((1, n_songs))
        _y[0, song["index"]] = 1
        y = [_y] * len(x)

        _song_test_embeddings[song["index"]] = {"x": x, "y": y}
        with open("song_test_embeddings.pkl", "wb") as f:
            pickle.dump(_song_test_embeddings, f)

        Y_val.extend(y)
        X_val.extend(x)

    Z_val = tf.data.Dataset.from_tensor_slices((X_val, Y_val))

    model.fit(Z, epochs=50, validation_data=Z_val)

    model.save("model.keras")
