import os.path

from InfraredController import InfraredController
from loguru import logger

BASE_PATH = os.path.dirname(__file__)


@logger.catch
def main():
    # Init the logger with a new file every day
    logger.add(
        BASE_PATH + "/logs/{time:YYYY_MM_DD}.log",
        format="{time:HH:mm:ss.SSS} | {level:^8} | {module}:{function}:{line} - {message}",
        rotation="12:00", enqueue=True, backtrace=True, diagnose=True,
    )

    runnable = InfraredController(BASE_PATH)
    runnable.run()


if __name__ == '__main__':
    main()
