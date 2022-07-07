# Bobarr-Convertium

Convertium is a simple python script which recursively looks for video files in configured directories, then automatically reformats them in a style to minimize transcoding, by maximising compatibility with as many devices as possible. Files will be automatically reformatted to the following file format:
```bash
fps = 30 #TODO: NOT IMPLEMENTED
container = .mp4
video codec = h264
audio codec = mp3 #TODO: this will eventually become acc or ac3
resolution = 1920x1080
```

These options, along with many others are configurable in [`config/general.toml`](config/general.toml).

## Installation
```bash
#TODO
```

## Remaining Project Goals
- [ ] improve logging (timestamps + log to file)
- [ ] improve configuration options for ffmpeg
- [ ] setup docker, and deployment scripts
- [ ] test suite

## Licensing and Contribution
Unless otherwise specified, all contributions will be licensed under MIT