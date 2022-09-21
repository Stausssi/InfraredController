import os.path
import sys

from loguru import logger

from InfraredController import InfraredController


@logger.catch
def main():
    # Init the logger with a new file every day
    logger.add(
        os.path.dirname(__file__) + "/logs/{time:YYYY_MM_DD}.log",
        format="{time:HH:mm:ss.SSS} | {level:^8} | {module}:{function}:{line} - {message}",
        rotation="12:00", enqueue=True, backtrace=True, diagnose=True,
    )
    logger.add(sys.stderr)

    runnable = InfraredController()
    runnable.run()


if __name__ == '__main__':
    main()
