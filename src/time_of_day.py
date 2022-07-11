import datetime
from typing import Tuple


class TimeAndThreads:
    def __init__(self, config: str) -> None:
        # Validate the config
        if config.count("-") != 1:
            raise ValueError(
                "The string must contain exactly one '-': {}".format(config)
            )

        # if string contains more than two T# error
        if config.count("T#") > 2:
            raise ValueError(
                "The string contains more than two 'T#': {}".format(config)
            )

        # split string into start and end times
        start_time, end_time = config.split("-")

        # split start threads from string
        if "T#" in start_time:
            start_time, start_threads = start_time.split("T#")
        else:
            start_threads = -1

        # split start_time into hours and minutes
        start_hours, start_minutes = start_time.split(":")

        # split end threads from string
        if "T#" in end_time:
            end_time, end_threads = end_time.split("T#")
        else:
            end_threads = -1

        # split end_time into hours and minutes
        end_hours, end_minutes = end_time.split(":")

        # validate start time is earlier than end time
        if start_time > end_time:
            raise ValueError("Start time is later than end time")

        # save config
        self.start_time = (int(start_hours), int(start_minutes))
        self.end_time = (int(end_hours), int(end_minutes))
        self.start_threads = int(start_threads)
        self.end_threads = int(end_threads)

    def get_time(self) -> Tuple[int, int]:
        """
        Get the current time, and return it in a 2-int tuple (hours, minutes)
        """
        now = datetime.datetime.now()
        return (int(now.strftime("%H")), int(now.strftime("%M")))

    def get_num_threads(self) -> int:
        """
        Get the number of threads to use, based on the current time. Will return -1 if infinite threads are allowed.
        """
        time = self.get_time()
        if time >= self.start_time and time <= self.end_time:
            return self.start_threads
        else:
            return self.end_threads

    def processing_enabled(self) -> bool:
        """
        Return True if processing is enabled at the current time, False otherwise.
        """
        num_threads = self.get_num_threads()
        if num_threads == -1 or num_threads > 0:
            return True
        return False
