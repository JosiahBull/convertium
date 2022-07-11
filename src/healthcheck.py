import time
import logging
from typing import Final

HEALTHCHECK_FAILURE_THRESHHOLD_MINUTES: Final[int] = 3
HEALTHCHECK_FILE_NAME: Final[str] = "healthcheck"


def ping() -> None:
    """
    Write the current timestamp to a file
    """
    logging.debug("Pinging healthcheck file")
    with open(HEALTHCHECK_FILE_NAME, "w") as f:
        f.write(str(time.time()))


def read_timestamp_from_file() -> float:
    """
    Read the timestamp from a file
    """
    try:
        with open(HEALTHCHECK_FILE_NAME, "r") as f:
            return float(f.read())
    except FileNotFoundError:
        return 0.0


def is_timestamp_valid(timestamp: float) -> bool:
    """
    Check if a timestamp is valid
    """
    return time.time() - timestamp < HEALTHCHECK_FAILURE_THRESHHOLD_MINUTES * 60


def healthcheck() -> None:
    """
    Check if the healthcheck file is valid
    """
    if is_timestamp_valid(read_timestamp_from_file()):
        exit(0)
    else:
        exit(1)


# only run if main
if __name__ == "__main__":  # pragma: no cover
    healthcheck()
