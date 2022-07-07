# Bobarr-Convertium

Convertium is a simple python script which recursively looks for video files in configured directories, then automatically reformats them in a style to minimize transcoding, by maximising compatibility with as many devices as possible. Files will be automatically reformatted to the following file format:
```bash
fps = 30
container = .mp4
video codec = h264
audio codec = mp3
resolution = 1920x1080
```

These options, along with many others are configurable in [`config/general.toml`](config/general.toml).

## Development
```bash
pip install -r requirements.txt
python ./src/convertium.py
```

## Usage
```bash
docker-compose up -d
```

## Remaining Project Goals
- [ ] improve logging (timestamps + log to file)
- [x] improve configuration options for ffmpeg
- [x] setup docker, and deployment scripts
- [ ] add healthcheck
- [ ] test suite
- [ ] build web dashboard

## Sister Projects
- [Bobarr-Renameium](https://github.com/JosiahBull/bobarr-renameium) - Rename files according to easily customizable and configurable standards.
- [Bobarr-Removeium](https://github.com/JosiahBull/bobarr-removeium) - Remove excess files provided in torrents, to clean up the database.
- [Bobarr-Subteium](https://github.com/JosiahBull/bobarr-subteium) - Automatically strip advertisements and insert subtitle files into videos.
- [Bobarr-Convertium](https://github.com/JosiahBull/bobarr-convertium) - Automatically convert files into a widely supported standard to reduce transcoding.

## Licensing and Contribution
Unless otherwise specified, all contributions will be licensed under MIT