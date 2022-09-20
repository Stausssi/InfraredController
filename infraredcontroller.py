import json
import sys
from threading import Thread
from loguru import logger


class InfraredController:
    def __init__(self):
        logger.info("Init")

    def run(self):
        thread = Thread(target=self.loop)
        thread.start()

        thread.join()

    def loop(self):
        for line in sys.stdin:
            self.handle_message(json.loads(line))

    def handle_message(self, message):
        logger.info(f"Received the message: {message}")

    def send(self, message):
        logger.info(f"Writing '{message}'")
        sys.stdout.write(json.dumps(message) + "\n")
        sys.stdout.flush()
