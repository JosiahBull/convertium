# Convertium

![Docker](https://github.com/JosiahBull/Convertium/actions/workflows/docker.yml/badge.svg)
![Lint](https://github.com/JosiahBull/Convertium/actions/workflows/lint.yml/badge.svg)
![Test](https://github.com/JosiahBull/Convertium/actions/workflows/test.yml/badge.svg)

Convertium is a simple python script which recursively looks for video files in configured directories, then automatically reformats them in a style to minimize transcoding, by maximizing compatibility with as many devices as possible. Files will be automatically reformatted to the following file format:
```bash
fps = 30
container = .mp4
video codec = h264
audio codec = mp3
resolution = 1920x1080
```

These options, along with many others are configurable in [`config/general.toml`](config/general.toml).

## Usage
```bash
git clone https://github.com/JosiahBull/convertium/
cd convertuim
# add volumes for all content you want to scan, along with other relevant options
nano docker-compose.yml
# tell program to scan those volumes
nano config/general.toml
# begin scanning
docker-compose up -d
```

## Sister Projects
- [Renameium](https://github.com/JosiahBull/renameium) - Rename files according to easily customizable and configurable standards.
- [Removeium](https://github.com/JosiahBull/removeium) - Remove excess files provided in torrents, to clean up the database.
- [Subteium](https://github.com/JosiahBull/subteium) - Automatically strip advertisements and insert subtitle files into videos.
- [Convertium](https://github.com/JosiahBull/convertium) - Automatically convert files into a widely supported standard to reduce transcoding.

## Licensing and Contribution
Unless otherwise specified, all contributions will be licensed under MIT