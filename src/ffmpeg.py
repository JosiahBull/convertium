import os
import logging
import healthcheck
from subprocess import Popen
from shutil import move
from tempfile import NamedTemporaryFile
from time import sleep


# TODO
def is_conversion_eligible(file_path: str) -> bool:
    """
    Check if a file is eligible for conversion, based on the type of media it is.
    If we are being strict, we could also run a validation on the file itself at this point too.
    """
    # return os.path.splitext(file_path)[1].lower() in ['.mp4', '.mov']


def convert(path: str, ffmpeg_args: list[str]) -> None:
    """
    Convert a video to a mp4 file.
    """
    global process_handle

    # create a temporary file
    with NamedTemporaryFile(mode="w+", delete=False, suffix='.mp4', ) as tmp_f:
        try:
            logging.debug('Converting {} to {}'.format(path, tmp_f.name))

            # perform replacements on ffmpeg arguments
            ffmpeg_args.insert(0, path)
            ffmpeg_args.insert(0, '-i')
            ffmpeg_args.insert(0, 'ffmpeg')
            ffmpeg_args.append(tmp_f.name)

            # Create a ffmpeg subprocess to encode the video
            logging.debug('ffmpeg arguments: {}'.format(ffmpeg_args))
            logging.debug('starting ffmpeg process')
            process_handle = Popen(ffmpeg_args)

            # wait for file to finish converting
            logging.debug('waiting for process to complete')
            while process_handle.poll() is None:
                sleep(5)
                healthcheck.ping()

            # check that process succeeded
            if process_handle.returncode != 0:
                raise Exception('ffmpeg process failed with return code {}'.format(process_handle.returncode))

            # Remove the original video
            logging.debug('removing original video')
            os.remove(path)

            # change extension on path variable to .mp4
            logging.debug('renaming output file')
            base = os.path.splitext(path)[0]

            # move the file
            move(tmp_f.name, base + '.mp4')
        except Exception as e:
            logging.exception('Error converting {}: {}'.format(path, e))
        finally:
            # delete the temporary file, if it still exists
            if os.path.exists(tmp_f.name):
                logging.debug('removing temporary file that still remains')
                os.remove(tmp_f.name)

            if process_handle is not None and process_handle.poll() is not None:
                process_handle.terminate()

            process_handle = None
