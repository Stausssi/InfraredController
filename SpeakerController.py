from typing import Callable

from loguru import logger

from ControllerBase import ControllerBase

IR_LED_PORT = 22


class SpeakerController(ControllerBase):
    def __init__(self, power_state=False, source_state=False, light_state=False):
        self.power = power_state
        self.source = source_state
        self.light = light_state

        logger.debug(f"Initialized with power: {self.power}, source: {self.source}, light: {self.light}")

        super().__init__(IR_LED_PORT, "speakers.json", "Speaker")

        self.message_handlers.update({
            "power": self._set_power,
            "source": self._set_source,
            "light": self._set_light
        })

    def _set_power(self, characteristic: str, value: bool):
        if self.power == value:
            return

        self.log_change("power", characteristic, value)
        self.power = value
        self.send_ir_command("power")

        # Automatically turn the light off on start
        if value:
            self.send_ir_command("light")

    def _set_source(self, characteristic: str, value: bool):
        if self.source == value:
            return

        self.log_change("source", characteristic, value)
        self.source = value
        self.send_ir_command("source")

    def _set_light(self, characteristic: str, value: bool):
        if self.light == value:
            return

        self.log_change("light", characteristic, value)
        self.light = value
        self.send_ir_command("light")
