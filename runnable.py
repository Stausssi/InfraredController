from infraredcontroller import InfraredController
from loguru import logger

if __name__ == '__main__':
    # Init the logger with a new file every day
    logger.add(
        "logs/{time:YYYY_MM_DD}.log",
        format="{time:HH:mm:ss.SSS} | {level: <8} | {module}:{function}:{line} - {message}",
        rotation="12:00", enqueue=True, backtrace=True, diagnose=True,
    )

    runnable = InfraredController()
    runnable.run()
