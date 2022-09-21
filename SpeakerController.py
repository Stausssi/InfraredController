from loguru import logger

from ControllerBase import ControllerBase


class SpeakerController(ControllerBase):
    def __init__(self, power_state = False, source_state = False, light_state = False):
        self.power = power_state
        self.source = source_state
        self.light = light_state

        super().__init__(22, "speakers.json")

        self.message_handlers.update({
            "power": self._set_power,
            "source": self._set_source,
            "light": self._set_light
        })

    def _set_power(self, characteristic: str, value: bool):
        logger.info(f"Power '{characteristic}' is now set to {value}")
        self.power = value

    def _set_source(self, characteristic: str, value: bool):
        logger.info(f"Source '{characteristic}' is now set to {value}")
        self.source = value

    def _set_light(self, characteristic: str, value: bool):
        logger.info(f"Light '{characteristic}' is now set to {value}")
        self.light = value
