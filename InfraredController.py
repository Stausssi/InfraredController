import json
import sys
from threading import Thread
from loguru import logger
from piir import Remote


class InfraredController:
    def __init__(self):
        self.SPEAKER_IR_PORT = 22
        self.CLOCK_IR_PORT = 22

        self.speaker_remote = Remote("speakers.json", self.SPEAKER_IR_PORT)
        self.clock_remote = Remote("clock.json", self.CLOCK_IR_PORT)

        self._messageHandlers = {
            "Speaker": {
                "Mute": self._toggle_speaker,
                "Active": self._toggle_light
            },
            "Clock": {
                "On": self._toggle_clock,
                "Brightness": self._set_brightness
            }
        }

    def run(self):
        thread = Thread(target=self.loop)
        thread.start()

        thread.join()

    def loop(self):
        for line in sys.stdin:
            self.handle_message(json.loads(line))

    def handle_message(self, message):
        self._messageHandlers[message["name"]][message["characteristic"]](message["value"])

    def _toggle_speaker(self, value):
        logger.debug(f"Speaker is now powered {'on' if value else 'off'}")
        self.speaker_remote.send("power")

    def _toggle_light(self, value):
        logger.debug(f"Speaker lighting is now powered {'on' if value else 'off'}")
        self.speaker_remote.send("light")

    def _toggle_clock(self, value):
        logger.debug(f"Clock is now powered {'on' if value else 'off'}")
        self.clock_remote.send("brightness")

    def _set_brightness(self, value):
        logger.debug(f"Clock brightness is now {value}")
        self.clock_remote.send("brightness")

    def send(self, message):
        logger.info(f"Writing '{message}'")
        sys.stdout.write(json.dumps(message) + "\n")
        sys.stdout.flush()
