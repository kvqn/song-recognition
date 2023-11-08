from tensorflow import keras
from model.create_model import (
    get_audio_embedding,
    get_text_embedding,
    combine_embeddings,
)


def predict(args):
    audio = args.audio
    lyrics = args.lyrics

    lyrics_embedding = get_text_embedding(lyrics)
    audio_embedding = get_audio_embedding(audio)
    combined_embedding = combine_embeddings(lyrics_embedding, audio_embedding)

    model = keras.models.load_model("model.keras")
    print(model.predict(combined_embedding))
