import os
import shutil
from typing import Final
import unittest
import src.ffmpeg as ffmpeg
import timeout_decorator

TEST_FOLDER_NAME: Final[str] = "./test_ffmpeg"
TEST_TIMEOUT: Final[int] = 60


class TestFfmpeg(unittest.TestCase):
    def setUp(self) -> None:
        # Create a folder for the test
        if not os.path.exists(TEST_FOLDER_NAME):
            os.mkdir(TEST_FOLDER_NAME)

        # Create a file to test with
        if not os.path.exists(TEST_FOLDER_NAME + "/test_video_1.mov"):
            shutil.copyfile(
                "./tests/assets/test_video_1.mov",
                TEST_FOLDER_NAME + "/test_video_1.mov",
            )

    @timeout_decorator.timeout(TEST_TIMEOUT)
    def test_valid_conversion(self) -> None:
        """
        Test that the conversion is valid
        """
        # Run the conversion
        ffmpeg.convert(
            TEST_FOLDER_NAME + "/test_video_1.mov",
            ["-c:v", "libx264", "-c:a", "copy", "-loglevel", "error", "-y"],
            -1,
        )

        # check for the converted file
        self.assertTrue(os.path.exists(TEST_FOLDER_NAME + "/test_video_1.mp4"))

        # check that previous video was deleted
        self.assertFalse(os.path.exists(TEST_FOLDER_NAME + "/test_video_1.mov"))

    def tearDown(self) -> None:
        """
        Remove the test folder
        """
        if os.path.exists(TEST_FOLDER_NAME):
            shutil.rmtree(TEST_FOLDER_NAME)


if __name__ == "__main__":
    unittest.main()
