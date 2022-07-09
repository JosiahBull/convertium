import os
import logging


class Config:
    def __init__(self):
        self.timezone: str = os.getenv("TIMEZONE", "Pacific/Auckland")
        self.log_level: str = os.getenv("LOG_LEVEL", "INFO").upper()
        self.valid_extensions: list[str] = os.getenv(
            "VALID_EXTENSIONS", ".mp4,.mkv,.avi,.mov,.wmv,.mpg,.mpeg"
        ).split(",")
        self.scan_interval: int = int(os.getenv("SCAN_INTERVAL", "20"))
        self.base_paths: list[str] = os.getenv("BASE_PATHS")
        self.ffmpeg_args: list[str] = os.getenv("FFMPEG_ARGUMENTS")

        if self.ffmpeg_args is None:
            logging.error("No ffmpeg arguments specified in config")
            exit(1)

        self.ffmpeg_args = self.ffmpeg_args.split(",")

        if self.base_paths is None:
            logging.error("No base paths specified in config")
            exit(1)

        self.base_paths = self.base_paths.split(",")

        # validate that the log level is valid
        if self.log_level not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            logging.error("Log level {} is not valid".format(self.log_level))
            exit(1)

        # validate the scan interval is reasonable
        if self.scan_interval < 1:
            logging.error("Scan interval {} is too low".format(self.scan_interval))
            exit(1)

        # validate that each of the base paths exist
        for base_path in self.base_paths:
            if not os.path.exists(base_path):
                logging.error("Base path {} does not exist".format(base_path))
                exit(1)

        # validate that each of the base paths contains at least one file
        for base_path in self.base_paths:
            if len(os.listdir(base_path)) == 0:
                logging.warning("Base path {} contains no files".format(base_path))
