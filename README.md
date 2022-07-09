# Convertium

![Docker](https://github.com/JosiahBull/Convertium/actions/workflows/docker.yml/badge.svg)
![Lint](https://github.com/JosiahBull/Convertium/actions/workflows/lint.yml/badge.svg)
![Test](https://github.com/JosiahBull/Convertium/actions/workflows/test.yml/badge.svg)
[![codecov](https://codecov.io/gh/JosiahBull/convertium/branch/main/graph/badge.svg?token=HGzsuaBxgi)](https://codecov.io/gh/JosiahBull/convertium)

Convertium is a simple python script which recursively looks for video files in configured directories, then automatically reformats them in a style to minimize transcoding, by maximizing compatibility with as many devices as possible. By default files will be automatically reformatted to the following file format:
```bash
fps = 30
container = .mp4
video codec = h264
audio codec = mp3
resolution = 1920x1080
```

## Usage

All environmental variables are configurable, but below is an example `docker-compose.yml` file.

```yaml
version: "3.9"
services:
  convertium:
    restart: unless-stopped
    image: ghcr.io/josiahbull/convertium:main
    volumes:
      - '/media/movies:/movies'
      - '/media/tv:/tv'
    environment:
      - TIMEZONE=Pacific/Auckland
      # DEBUG, INFO, WARN, ERROR, CRITICAL
      - LOG_LEVEL=INFO
      # number of minutes between scans
      - SCAN_INTERVAL=20
      # comma separated list of paths to scan
      - BASE_PATHS=/movies,/tv
      # comma separated list of extensions to attempt conversions on
      - VALID_EXTENSIONS=.mp4,.mkv,.avi,.mov,.wmv,.mpg,.mpeg
      # comma seperated list of ffmpeg arguments to pass when converting
      - FFMPEG_ARGUMENTS=-c:v,libx264,-crf,20,-preset,slow,-c:a,mp3,-b:a,192k,-vf,scale=1920:1080,-movflags,+faststart,-loglevel,error,-y
      - PYTHON_ENV=production
    depends_on:
      - postgres

  postgres:
    restart: unless-stopped
    image: postgres
    volumes:
      - './data:/var/lib/postgresql/data'
    environment:
      - POSTGRES_USER=convertium
      - POSTGRES_PASSWORD=convertium
      - POSTGRES_DB=convertium

  autoheal:
    restart: unless-stopped
    image: willfarrell/autoheal
    environment:
      - AUTOHEAL_CONTAINER_LABEL=all
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    depends_on:
      - convertium
      - postgres

```

Then simply run `docker-compose up -d` to begin scanning and converting files. Note that this process can be very cpu intensive, as this crate makes no attempt to utilise any hardware support.

## Sister Projects
- [Renameium](https://github.com/JosiahBull/renameium) - Rename files according to easily customizable and configurable standards.
- [Removeium](https://github.com/JosiahBull/removeium) - Remove excess files provided in torrents, to clean up the database.
- [Subteium](https://github.com/JosiahBull/subteium) - Automatically strip advertisements and insert subtitle files into videos.
- [Convertium](https://github.com/JosiahBull/convertium) - Automatically convert files into a widely supported standard to reduce transcoding.

## Licensing and Contribution
Unless otherwise specified, all contributions will be licensed under MIT
