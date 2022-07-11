import os

if os.getenv("PYTHON_ENV") == "production":
    import healthcheck
    import database
    import config
    import ffmpeg
    import time_of_day
else:
    import src.healthcheck as healthcheck
    import src.database as database
    import src.config as config
    import src.ffmpeg as ffmpeg
    import src.time_of_day as time_of_day


import logging
from time import sleep
import time
from psutil import Popen
import signal


def handler(_signum: int, _frame) -> None:
    """
    Signal handler
    """
    global process_handle
    if process_handle is not None:
        process_handle.terminate()
    logging.info("Exiting")
    exit(0)


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
    file_list: list[str] = [
        file
        for file in file_list
        if os.path.splitext(file)[1].lower() in valid_extensions
    ]

    return file_list


def main(run_once=False) -> None:
    """
    Main function
    """
    # Set handlers
    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)

    # Set up logging
    logFormatter = logging.Formatter(
        "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s"
    )
    rootLogger = logging.getLogger()

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)

    # Load config
    env_vars = config.Config()

    sleep_time = env_vars.scan_interval * 60

    rootLogger.setLevel(env_vars.log_level)

    # create database
    db = database.Database()

    # create timer
    timer = time_of_day.TimeAndThreads(os.environ["CONVERSION_TIMES"])

    # For each base path, get a list of files to process then process them
    while True:
        start_time = time.time()
        for base_path in env_vars.base_paths:
            # ping healthcheck
            healthcheck.ping()

            logging.info("Checking base path: {}".format(base_path))
            # collect file list
            file_list: list[str] = generate_scan_list(
                base_path, env_vars.valid_extensions
            )

            # filter files for those which do not require conversion
            file_list: list[str] = [file for file in file_list if not db.contains(file)]

            # convert files
            for file in file_list:
                if not timer.processing_enabled():
                    logging.info("Processing is not enabled at this time")
                    while not timer.processing_enabled():
                        sleep(2)

                # check that file exists
                if not os.path.isfile(file):
                    logging.error("File does not exist: {}".format(file))
                    continue

                logging.info("Converting {}".format(file))
                ffmpeg.convert(
                    file, env_vars.ffmpeg_args.copy(), timer.get_num_threads()
                )
                db.add(file)
                logging.info("Completed conversion for {}".format(file))
        logging.info("Completed in %.2f seconds" % (time.time() - start_time))
        logging.info(
            "Sleeping for {} minutes before scanning again".format(int(sleep_time / 60))
        )

        if run_once:
            break

        # wait for sleep_time but ping healthcheck every now and then
        for _ in range(int(sleep_time / 5)):
            healthcheck.ping()
            sleep(5)


global process_handle
process_handle: Popen = None

if __name__ == "__main__":
    main()
