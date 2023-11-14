from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated, Optional

from .create_model import (
    get_audio_embedding,
    get_text_embedding,
    get_empty_text_embedding,
    get_empty_audio_embedding,
)
from model.predict import predict_from_embedding
import aiofiles
import uuid
import os
import shutil
import pandas as pd
from model import DATASET_DIR_PATH


app = FastAPI()

origins = [
    # "http://localhost:5173",
    "*",
    # "https://localhost.tiangolo.com",
    # "http://localhost",
    # "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.post("/predict")
# async def predict(audio: Annotated[bytes, Form()], text: Annotated[str, Form()]):
#     print(audio, text)
#     return {"song": "a", "artist": "b", "confidence": "c"}


@app.post("/predict/audio-and-text")
async def predict_audio_and_text(
    audio: Annotated[UploadFile, Form()],
    text: Annotated[str, Form()],
):
    save_path = os.path.join(".saved", f"{uuid.uuid4()}.wav")
    with open(save_path, "wb") as file:
        shutil.copyfileobj(audio.file, file)
    audio_embedding = get_audio_embedding(save_path)
    text_embedding = get_text_embedding(text)
    prediction = predict_from_embedding(audio_embedding, text_embedding)
    return {
        "song": prediction["song"],
        "artist": prediction["artist"],
        "confidence": float(prediction["confidence"]),
        "thumbnail_url": prediction["thumbnail_url"],
        "youtube_url": prediction["youtube_url"],
    }


@app.post("/predict/audio")
async def predict_audio(
    audio: Annotated[UploadFile, Form()],
):
    save_path = os.path.join(".saved", f"{uuid.uuid4()}.wav")
    with open(save_path, "wb") as file:
        shutil.copyfileobj(audio.file, file)
    audio_embedding = get_audio_embedding(save_path)
    text_embedding = get_empty_text_embedding()
    prediction = predict_from_embedding(audio_embedding, text_embedding)
    return {
        "song": prediction["song"],
        "artist": prediction["artist"],
        "confidence": float(prediction["confidence"]),
        "thumbnail_url": prediction["thumbnail_url"],
        "youtube_url": prediction["youtube_url"],
    }


@app.post("/predict/text")
async def predict_text(
    text: Annotated[str, Form()],
):
    audio_embedding = get_empty_audio_embedding()
    text_embedding = get_text_embedding(text)
    prediction = predict_from_embedding(audio_embedding, text_embedding)
    return {
        "song": prediction["song"],
        "artist": prediction["artist"],
        "confidence": float(prediction["confidence"]),
        "thumbnail_url": prediction["thumbnail_url"],
        "youtube_url": prediction["youtube_url"],
    }


@app.get("/songs")
async def songs():
    df = pd.read_csv(os.path.join(DATASET_DIR_PATH, "dataset.csv"))
    songs = []
    for _, song in df.iterrows():
        songs.append(
            {
                "song": song["title"],
                "artist": song["artist"],
                "thumbnail_url": song["thumbnail_url"],
                "youtube_url": song["youtube_url"],
            }
        )

    return {"songs": songs}


def start_server(args):
    if not os.path.exists(".saved"):
        os.mkdir(".saved")

    import uvicorn

    uvicorn.run("model.server:app", reload=args.reload, host="0.0.0.0")
