import subprocess
import os
import shutil
import logging
from time import sleep
import time
from psutil import Popen
import toml
import database
import signal
import tempfile

def handler(_signum: int, _frame) -> None:
    """
    Signal handler
    """
    global process_handle
    if process_handle is not None:
        process_handle.terminate()
    logging.info('Exiting')
    exit(0)

def convert(path: str, ffmpeg_args: list[str]) -> None:
    """
    Convert a video to a mp4 file.
    """

    global process_handle

    # create a temporary file
    with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix='.mp4', ) as tmp_f:
        try:
            # perform replacements on ffmpeg arguments
            ffmpeg_args = [arg.replace('%INPUT_FILE%', path, 1) for arg in ffmpeg_args]
            ffmpeg_args = [arg.replace('%OUTPUT_NAME%', tmp_f.name, 1) for arg in ffmpeg_args]

            # Create a ffmpeg subprocess to encode the video
            process_handle = subprocess.Popen(ffmpeg_args)

            # wait for file to finish converting
            process_handle.wait()
            process_handle = None

            # Remove the original video
            os.remove(path)

            # change extension on path variable to .mp4
            base = os.path.splitext(path)[0]

            # move the file
            logging.info("trying to move")
            shutil.move(tmp_f.name, base + '.mp4')
        finally:
            # delete the temporary file, if it still exists
            if os.path.exists(tmp_f.name):
                os.remove(tmp_f.name)

def generate_scan_list(base_path: str, valid_extensions: list[str]) -> list[str]:
    """
    Recursively walk every file inside of a given base path, and return them in a flattened list
    """
    # Get the list of files in the base path
    file_list = []
    for root, _, files in os.walk(base_path):
        for file in files:
            file_list.append(os.path.join(root, file))

    # Filter out files that don't have the correct extension
    file_list: list[str] = [file for file in file_list if os.path.splitext(file)[1].lower() in valid_extensions]

    return file_list

def main():
    """
    Main function
    """
    # Set handlers
    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)

    # Load config
    config = toml.load('config/general.toml')

    # Get the list of files to process
    log_level: str = config.get('log_level')

    if log_level is None:
        logging.error('No log level specified in config')
        exit(1)

    valid_extensions: list[str] = config.get('valid_extensions')

    if valid_extensions is None:
        logging.error('No valid extensions specified in config')
        exit(1)

    base_paths: list[str] = config.get('base_paths')

    if base_paths is None:
        logging.error('No base paths specified in config')
        exit(1)

    sleep_time: int = config.get('check_interval_minutes') * 60

    if sleep_time is None:
        logging.error('Sleep time is not set in config')
        exit(1)

    # Load ffmpeg config
    ffmpeg_args: list[str] = config.get('ffmpeg_arguments')

    if ffmpeg_args is None:
        logging.error('No ffmpeg arguments found in config')
        exit(1)

    # Set up logging
    logging.basicConfig(level=log_level)

    # create database
    db = database.Database()

    # For each base path, get a list of files to process then process them
    while True:
        start_time = time.time()
        for base_path in base_paths:
            logging.info('Checking base path: {}'.format(base_path))
            # collect file list
            file_list: list[str] = generate_scan_list(base_path, valid_extensions)

            # filter files for those which do not require conversion
            file_list: list[str] = [file for file in file_list if not db.contains(file)]

            # convert files
            for file in file_list:
                try:
                    logging.info('Converting {}'.format(file))
                    convert(file, ffmpeg_args)
                    db.add(file)
                except Exception as e:
                    logging.error('Error converting {}: {}'.format(file, e))
                    if process_handle is not None:
                        process_handle.terminate()
                finally:
                    logging.info('Completed conversion for {}'.format(file))
        logging.info('Completed in %.2f seconds' % (time.time() - start_time))
        logging.info('Sleeping for {} minutes before scanning again'.format(int(sleep_time / 60)))
        sleep(sleep_time)

process_handle: Popen = None

main()