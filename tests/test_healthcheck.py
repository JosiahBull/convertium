import os
import time
import unittest
import src.healthcheck as healthcheck


class TestHealthCheck(unittest.TestCase):
    def setUp(self) -> None:
        # remove any existing healthcheck file
        if os.path.isfile("healthcheck"):
            os.remove("healthcheck")

    def test_ping(self) -> None:
        """
        Test that the healthcheck file is created
        """
        healthcheck.ping()
        self.assertTrue(os.path.isfile("healthcheck"))
        # validate the timestamp is from just now
        with open("healthcheck", "r") as f:
            timestamp = f.read()
            self.assertTrue(float(timestamp) > 0)
            self.assertTrue(time.time() - float(timestamp) < 2)

    def test_read_timestamp_from_file(self) -> None:
        """
        Test that the timestamp is read from the file
        """
        with open("healthcheck", "w") as f:
            f.write("1")
        self.assertEqual(healthcheck.read_timestamp_from_file(), 1)

    def test_is_timestamp_valid(self) -> None:
        """
        Test that the timestamp is valid
        """
        self.assertTrue(healthcheck.is_timestamp_valid(time.time()))
        self.assertFalse(
            healthcheck.is_timestamp_valid(
                time.time() - healthcheck.HEALTHCHECK_FAILURE_THRESHHOLD_MINUTES * 60
            )
        )

    def test_healthcheck(self) -> None:
        """
        Test that the healthcheck function exits with 0 if the timestamp is valid
        """
        # set invalid timestamp
        current_time = (
            time.time() - healthcheck.HEALTHCHECK_FAILURE_THRESHHOLD_MINUTES * 60
        )
        with open("healthcheck", "w") as f:
            f.write(str(current_time))
        with self.assertRaises(SystemExit) as cm:
            healthcheck.healthcheck()
        self.assertEqual(cm.exception.code, 1)

        # set valid timestamp
        with open("healthcheck", "w") as f:
            f.write(str(time.time()))
        with self.assertRaises(SystemExit) as cm:
            healthcheck.healthcheck()
        self.assertEqual(cm.exception.code, 0)

    def test_healthcheck_with_no_file(self) -> None:
        """
        Test that the healthcheck function exits with 1 if the file does not exist
        """
        # remove any existing healthcheck file
        if os.path.isfile("healthcheck"):
            os.remove("healthcheck")
        value = healthcheck.read_timestamp_from_file()
        self.assertEqual(value, 0.0)

    def tearDown(self) -> None:
        # remove any existing healthcheck file
        if os.path.isfile("healthcheck"):
            os.remove("healthcheck")


if __name__ == "__main__":
    unittest.main()
