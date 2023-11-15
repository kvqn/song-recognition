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

```
git clone https://github.com/kvqn/song-recognition
cd song-recognition
```

### 3. (optional) create a virtual environment.

Creating a virtual environment is recommended for most python projects so that
dependencies don't conflict with other projects. 
Many people prefer to use `conda` however `venv` can work just fine.

```
python -m venv .venv
source .venv/bin/activate
```

### 4. Install python dependencies

This will take some time.

```
pip install -r requirements.txt
```

### 5. Install node dependencies

We prefer to use `bun` as it is way faster than any alternative. If you don't
have it installed, you can install it with `npm i -g bun`. \
However `npm` will also do just fine.

```
bun i
# or
npm i
```

### Start the python server

The first startup takes some time as it downloads further dependencies.

```
python -m model start-server
```

### Start the web server

```
cd app
npm run dev
```

```

## Dataset

The dataset, as you might have guessed, was not easily available.

So I wrote a script to scrape it.

### Scraping

Use the CLI. It's pretty straight forward.

`py -m scraper`
```
