import json
import sys
from threading import Thread
from typing import Union, Dict

from loguru import logger

from ClockController import ClockController
from SpeakerController import SpeakerController


class InfraredController:
    def __init__(self):
        self.SPEAKER_IR_PORT = 22
        self.CLOCK_IR_PORT = 22

        self.speaker_controller = SpeakerController()
        self.clock_controller = ClockController()

        self._controllers = {
            "speaker": self.speaker_controller,
            "clock": self.clock_controller
        }

    def run(self):
        thread = Thread(target=self.loop)
        thread.start()

        thread.join()

    def loop(self):
        for line in sys.stdin:
            self.handle_message(json.loads(line))

    def handle_message(self, message: Dict[str, Union[bool, str, int, Dict[str, Union[bool, str, int]]]]):
        name: str = message["name"].lower()
        target, acc_type = name.split("_", 1)

        self._controllers.get(target).handle_message(
            acc_type, message["characteristic"].lower(), message["value"], message["status"]
        )

    def send(self, message):
        logger.info(f"Writing '{message}'")
        sys.stdout.write(json.dumps(message) + "\n")
        sys.stdout.flush()
