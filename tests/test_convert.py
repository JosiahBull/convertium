from typing import Final
import unittest
import shutil
import os
import psycopg2
import src.convertium as convertium
import timeout_decorator

TEST_FOLDER_NAME: Final[str] = "./test_convert"
TEST_TIMEOUT: Final[int] = 60


class TestConvert(unittest.TestCase):
    def setUp(self):
        """
        Setup the environment variables for the test
        """
        # Create a folder for the test
        if not os.path.exists(TEST_FOLDER_NAME):
            os.mkdir(TEST_FOLDER_NAME)

        # Create a file to test with
        if not os.path.exists(TEST_FOLDER_NAME + "/test_video_1.mov"):
            shutil.copyfile(
                "./tests/assets/test_video_1.mov",
                TEST_FOLDER_NAME + "/test_video_1.mov",
            )

        # Save all existing environment variables
        self.old_env = os.environ.copy()

        # Set all Environmental variables
        os.environ["TIMEZONE"] = "Pacific/Auckland"
        os.environ["LOG_LEVEL"] = "DEBUG"
        os.environ["SCAN_INTERVAL"] = "20"
        os.environ["BASE_PATHS"] = TEST_FOLDER_NAME
        os.environ["VALID_EXTENSIONS"] = ".mov"
        os.environ["FFMPEG_ARGUMENTS"] = "-c:v,libx264,-c:a,copy,-loglevel,error,-y"
        os.environ[
            "CONVERSION_TIMES"
        ] = "00:00-01:00"  # always active with maximum threads

        os.environ["CONVERTIUM_DB_USER"] = "convertium"
        os.environ["CONVERTIUM_DB_PASSWORD"] = "convertium"
        os.environ["CONVERTIUM_DB_HOST"] = os.getenv("CONVERTIUM_DB_HOST", "localhost")
        os.environ["CONVERTIUM_DB_PORT"] = "5432"
        os.environ["CONVERTIUM_DB_DNNAME"] = "convertium_test"

        # remove entry from the database
        with psycopg2.connect(
            user="convertium",
            password="convertium",
            host=os.getenv("CONVERTIUM_DB_HOST", "localhost"),
            port=5432,
            dbname="convertium_test",
        ) as conn:
            with conn.cursor() as curr:
                curr.execute("DROP TABLE IF EXISTS paths;")

    @timeout_decorator.timeout(TEST_TIMEOUT)
    def test_valid_conversion(self):
        """
        Test that the conversion is valid
        """

        # Run the conversion
        convertium.main(True)

        # check for the converted file
        self.assertTrue(os.path.exists(TEST_FOLDER_NAME + "/test_video_1.mp4"))

        # check that previous video was deleted
        self.assertFalse(os.path.exists(TEST_FOLDER_NAME + "/test_video_1.mov"))

        # validate database was updated
        with psycopg2.connect(
            user="convertium",
            password="convertium",
            host=os.getenv("CONVERTIUM_DB_HOST", "localhost"),
            port=5432,
            dbname="convertium_test",
        ) as conn:
            with conn.cursor() as curr:
                curr.execute(
                    "SELECT * FROM paths WHERE path = %s;",
                    (TEST_FOLDER_NAME + "/test_video_1.mov",),
                )
                self.assertTrue(curr.rowcount > 0)

    def tearDown(self):
        """
        Clean up the environment variables for the test
        """

        # Remove the folder for the test
        if os.path.exists(TEST_FOLDER_NAME):
            shutil.rmtree(TEST_FOLDER_NAME)

        # Restore all environment variables
        os.environ.clear()
        os.environ.update(self.old_env)


if __name__ == "__main__":
    unittest.main()
