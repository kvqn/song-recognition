# Song Recognition

This project aims to create a neural network and application that feeds on multi
modal inputs to identify songs.

You can host it for yourself by following the
[Quick Start Guide](#quick-start-guide)

## Quick Start Guide

### 1. Install the system dependencies

You will need Python and NodeJS.

> The project is tested on python 3.11.5 and node 21.1.0

### 2. Clone the repository

```sh
git clone https://github.com/kvqn/song-recognition
cd song-recognition
```

### 3. (optional) create a virtual environment

Creating a virtual environment is recommended for most python projects so that
dependencies don't conflict with other projects.
Many people prefer to use `conda` however `venv` can work just fine.

```sh
python -m venv .venv
source .venv/bin/activate
```

### 4. Install python dependencies

This will take some time.

```sh
pip install -r requirements.txt
```

### 5. Install node dependencies

We prefer to use `bun` as it is way faster than any alternative. If you don't
have it installed, you can install it with `npm i -g bun`. \
However `npm` will also do just fine.

```sh
bun i
# or
npm i
```

### Start the python server

The first startup takes some time as it downloads further dependencies.

```sh
python -m model start-server
```

### Start the web server

```sh
cd app
npm run dev
```

### Using the application

You can record or upload 5 seconds of audio and a piece of lyrics. The model will
then try to identify the song. You can also see the model's confidence in the
prediction. Check the `Songs Archive` tab to see all the songs that the model has been
trained on.

## Command Line

I made several command line tools to help with the development of the project.

### Scraping CLI

To create the dataset, I created a scraping tool that uses [yt-dlp](https://github.com/yt-dlp/yt-dlp) and [azapi](https://github.com/elmoiv/azapi) to download songs and lyrics from YouTube and AZLyrics respectively.

#### Add a song

```sh
python -m scraper add song <song url>
```

#### Add a playlist

```sh
python -m scraper add playlist <playlist url>
```

#### List all songs

```sh
python -m scraper list
```

#### Remove a song

```sh
python -m scraper remove <song id>
```

### Model CLI

Command line interface to interact with the model.

#### Create a dataset

Once you have your songs in the `database/` folder using the [scraping CLI](#scraping-cli), you can create a dataset.

This command will create 5 seconds clips of each song and save them in the `dataset/` folder.

You would need to have [ffmpeg](https://github.com/FFmpeg/FFmpeg) installed.

```sh
python -m model create-dataset
```

#### Train the model

To train the model, you need to have a dataset created.

```sh
python -m model create-model
```

#### Run a prediction

This command would run a prediction on a given audio file and lyrics.

You need to have a `model.keras` file either downloaded or created before executing this command.

```sh
python -m model predict <audio file> <lyrics>
```

> This method is not recommended as it would load the model every time you run it. \
> Instead, you can start the server and use the API to run predictions. See [Quick Start](#quick-start-guide).

#### Start server

This command would start a server that you can use to run predictions. It would load the model once and keep it in memory.

```sh
python -m model start-server
```

Now once you have the python server running, you can also go ahead and start the web server.

```sh
cd app
npm run dev
```
