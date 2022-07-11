import datetime
import unittest

from src.time_of_day import TimeAndThreads


class TestTimeAndThreads(unittest.TestCase):
    def test_get_num_threads_between_start_end(self):
        """
        This function will test that the correct amount of threads are returned between the start and end time
        """

        # construct the config string
        now = datetime.datetime.now()
        hours, minutes = int(now.strftime("%H")), int(now.strftime("%M"))

        # subtract one hour from the time, looping if appropriate
        starting_hours, ending_hours = hours, hours
        if hours == 0:
            starting_hours = 23
        else:
            starting_hours -= 1

        # add one hour to the time, looping if appropriate
        if hours == 23:
            ending_hours = 0
        else:
            ending_hours += 1

        # construct the config string
        config = f"{starting_hours}:{minutes}T#4-{ending_hours}:{minutes}T#0"

        # create the TimeAndThreads object
        time_and_threads = TimeAndThreads(config)

        # get the number of threads
        num_threads = time_and_threads.get_num_threads()

        # check that the number of threads is between the start and end time
        self.assertTrue(time_and_threads.processing_enabled())
        self.assertEqual(num_threads, 4)

    def test_get_num_threads_between_end_start(self):
        """
        This function will test that the correct amount of threads are returned between the end and start time
        """

        # construct the config string
        now = datetime.datetime.now()
        hours, minutes = int(now.strftime("%H")), int(now.strftime("%M"))

        starting_hours, ending_hours = hours, hours

        # subtract two hours from the time, looping if appropriate
        if hours == 1:
            starting_hours = 23
        elif hours == 0:
            starting_hours = 22
        else:
            starting_hours -= 2

        # subtract one hour from the time, looping if appropriate
        if hours == 0:
            ending_hours = 23
        else:
            ending_hours -= 1

        # construct the config string
        config = f"{starting_hours}:{minutes}T#0-{ending_hours}:{minutes}T#4"

        # create the TimeAndThreads object
        time_and_threads = TimeAndThreads(config)

        # get the number of threads
        num_threads = time_and_threads.get_num_threads()

        # check that the number of threads is between the start and end time
        self.assertEqual(num_threads, 4)

    def test_processing_disabled_when_no_threads(self):
        """
        This function will test that the processing is disabled when there are no threads
        """

        # construct the config string
        now = datetime.datetime.now()
        hours, minutes = int(now.strftime("%H")), int(now.strftime("%M"))

        # construct the config string
        config = f"{hours}:{minutes}T#0-{hours}:{minutes}T#0"

        # create the TimeAndThreads object
        time_and_threads = TimeAndThreads(config)

        # get the number of threads
        num_threads = time_and_threads.get_num_threads()

        # check that the number of threads is between the start and end time
        self.assertFalse(time_and_threads.processing_enabled())
        self.assertEqual(num_threads, 0)

    def test_no_threads_returns_infinite(self):
        """
        This function will test that the number of threads is infinite when there are no threads
        """

        # construct the config string
        now = datetime.datetime.now()
        hours, minutes = int(now.strftime("%H")), int(now.strftime("%M"))

        # construct the config string
        config = f"{hours}:{minutes}-{hours}:{minutes}"

        # create the TimeAndThreads object
        time_and_threads = TimeAndThreads(config)

        # get the number of threads
        num_threads = time_and_threads.get_num_threads()

        # check that the number of threads is between the start and end time
        self.assertEqual(num_threads, -1)
        self.assertTrue(time_and_threads.processing_enabled())


if __name__ == "__main__":
    unittest.main()
