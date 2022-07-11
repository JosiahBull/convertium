import os
import shutil
from typing import Final
import unittest
from src.config import Config

TEST_FOLDER_NAME: Final[str] = "./test_config"


class TestConfig(unittest.TestCase):
    def setUp(self):
        """
        Setup the environment variables for the test
        """

        # remove temporary folder
        if os.path.exists(TEST_FOLDER_NAME):
            shutil.rmtree(TEST_FOLDER_NAME)

        # Save all existing environment variables
        self.old_env = os.environ.copy()

        # Set all Environmental variables
        os.environ["TIMEZONE"] = "Pacific/Auckland"
        os.environ["LOG_LEVEL"] = "DEBUG"
        os.environ["SCAN_INTERVAL"] = "20"
        os.environ["BASE_PATHS"] = "tests"
        os.environ["VALID_EXTENSIONS"] = ".mov"
        os.environ["FFMPEG_ARGUMENTS"] = "-c:v,libx264,-c:a,copy,-y"

    def test_timezone(self) -> None:
        """
        Test that the timezone is valid
        """
        cfg = Config()
        self.assertEqual(cfg.timezone, "Pacific/Auckland")

    def test_log_level(self) -> None:
        """
        Test that the log level is valid
        """
        cfg = Config()
        self.assertEqual(cfg.log_level, "DEBUG")

    def test_invalid_log_level(self) -> None:
        """
        Test that the log level is invalid
        """
        os.environ["LOG_LEVEL"] = "INVALID"
        with self.assertRaises(SystemExit):
            Config()
        os.environ["LOG_LEVEL"] = "DEBUG"

    def test_scan_interval(self) -> None:
        """
        Test that the scan interval is valid
        """
        cfg = Config()
        self.assertEqual(cfg.scan_interval, 20)

    def test_invalid_scan_interval(self) -> None:
        """
        Test that the scan interval is invalid
        """
        os.environ["SCAN_INTERVAL"] = "0"
        with self.assertRaises(SystemExit):
            Config()

        os.environ["SCAN_INTERVAL"] = "INVALID"
        with self.assertRaises(ValueError):
            Config()

        os.environ["SCAN_INTERVAL"] = "20"

    def test_base_paths(self) -> None:
        """
        Test that the base paths are valid
        """
        cfg = Config()
        self.assertEqual(cfg.base_paths, ["tests"])

    def test_invalid_base_paths(self) -> None:
        """
        Test that the base paths are invalid
        """
        os.environ["BASE_PATHS"] = "./some_random_path"
        with self.assertRaises(SystemExit):
            Config()

        os.environ["BASE_PATHS"] = ""
        with self.assertRaises(SystemExit):
            Config()

        del os.environ["BASE_PATHS"]
        with self.assertRaises(SystemExit):
            Config()

        os.mkdir(TEST_FOLDER_NAME)
        os.environ["BASE_PATHS"] = TEST_FOLDER_NAME
        Config()  # XXX: can we validate that the warnign is printed?
        os.rmdir(TEST_FOLDER_NAME)

        os.environ["BASE_PATHS"] = "tests"

    def test_valid_extensions(self) -> None:
        """
        Test that the valid extensions are valid
        """
        cfg = Config()
        self.assertEqual(cfg.valid_extensions, [".mov"])

    def test_ffmpeg_arguments(self) -> None:
        """
        Test that the ffmpeg arguments are valid
        """
        cfg = Config()
        self.assertEqual(cfg.ffmpeg_args, ["-c:v", "libx264", "-c:a", "copy", "-y"])

    def test_invalid_ffmpeg_arguments(self) -> None:
        """
        Test that the ffmpeg arguments are invalid
        """
        del os.environ["FFMPEG_ARGUMENTS"]
        with self.assertRaises(SystemExit):
            Config()
        os.environ["FFMPEG_ARGUMENTS"] = "-c:v,libx264,-c:a,copy,-y"

    def tearDown(self) -> None:
        """
        Restore the environment variables
        """
        # Restore all environment variables
        os.environ.clear()
        os.environ.update(self.old_env)

        # remove temporary folder
        if os.path.exists(TEST_FOLDER_NAME):
            shutil.rmtree(TEST_FOLDER_NAME)


if __name__ == "__main__":
    unittest.main()
