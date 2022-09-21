from enum import IntEnum
from typing import Union

from loguru import logger

from ControllerBase import ControllerBase


class ClockController(ControllerBase):
    def __init__(self, brightness=0, light_on=False, rotate=False, show_temperature=False, flash_dot=False):
        self.brightness = brightness
        self.is_light_on = light_on
        self.rotate = rotate
        self.show_temperature = show_temperature
        self.flash_dot = flash_dot

        # The current state is determined by the brightness. Reverse the list because of the <= comparison
        self._light_state = self.__determine_light_state()

        logger.debug(
            f"Initialized with brightness {brightness} (state: {self._light_state.name}), rotation: {rotate}, "
            f"show temperature: {show_temperature}, flashing dot: {flash_dot}"
        )

        super().__init__(22, "clock.json", "Clock")

        self.message_handlers.update({
            "light": self._set_brightness,
            "rotation": self._set_rotation,
            "temp": self._set_show_temperature,
            "flashing_dot": self._set_flashing_dot
        })

    def __determine_light_state(self):
        """
        Determine the state of the clock light depending on the brightness.

        :return: The state of the light
        :rtype: ClockLightState
        """

        if self.is_light_on:
            return [state for state in reversed(ClockLightState) if self.brightness <= state][0]
        else:
            return ClockLightState.OFF

    def _set_brightness(self, characteristic: str, value: Union[int, bool]):
        self.log_change("brightness", characteristic, value)

        if "On" in characteristic:
            self.is_light_on = value
        else:
            self.brightness = value

        logger.info(f"Changing light state from '{self._light_state.name}' to '{self.__determine_light_state().name}'")

        # For every step we changed in the brightness level we have to send an IR signal
        self.send_ir_command("brightness", self._light_state - self.__determine_light_state())

        self._light_state = self.__determine_light_state()

    def _set_rotation(self, characteristic: str, value: bool):
        self.log_change("rotation", characteristic, value)
        self.rotate = value
        self.send_ir_command("rotation")

        # TODO: Consider implementing a different rotation with just clock and temperature by alternating
        #  the only problem would be the clicking sound

    def _set_show_temperature(self, characteristic: str, value: bool):
        self.log_change("show temperature", characteristic, value)
        self.show_temperature = value

        # Send the clock command to disable the temperature
        self.send_ir_command("temperature" if self.show_temperature else "clock")

    def _set_flashing_dot(self, characteristic: str, value: bool):
        self.log_change("flashing dot", characteristic, value)
        self.flash_dot = value
        self.send_ir_command("flashing_dot")


class ClockLightState(IntEnum):
    AUTO = 100
    BRIGHT = 99
    MEDIUM = 50
    DULL = 25
    OFF = 0

    @staticmethod
    def _get_step_map():
        return {
            ClockLightState.BRIGHT: 4,
            ClockLightState.MEDIUM: 3,
            ClockLightState.DULL: 2,
            ClockLightState.AUTO: 1,
            ClockLightState.OFF: 0
        }

    def __sub__(self, other):
        """
        This method returns how many steps are between both enums.

        The problem is ``AUTO`` since the clock works in the order of ``BRIGHT -> MEDIUM -> DULL -> AUTO -> OFF``

        The steps work like this:
            * ``BRIGHT`` -> ``MEDIUM`` = 2
            * ``MEDIUM`` -> ``BRIGHT`` = 3
            * ``AUTO`` -> ``OFF`` = 1

        :param other: The enum we are comparing ourselves to
        :type other: ClockLightState
        :return: The difference between the states
        """

        diff = self._get_step_map().get(self) - self._get_step_map().get(other)

        # We have to add five if we go from a lower to higher brightness because of the cycle
        if diff < 0:
            diff += 5

        return diff


# if __name__ == '__main__':
#     controller = ClockController(brightness=100, light_on=True)
#
#     controller.send_ir_command("brightness", 2)
#
#     print(f"Bright to Auto: {ClockLightState.BRIGHT - ClockLightState.AUTO}")
#     print(f"Auto to Medium: {ClockLightState.AUTO - ClockLightState.MEDIUM}")
#     print(f"Dull to Dull: {ClockLightState.DULL - ClockLightState.DULL}")
#     print(f"Auto to Off: {ClockLightState.AUTO - ClockLightState.OFF}")
#     print(f"Auto to Dull: {ClockLightState.AUTO - ClockLightState.DULL}")
#     print(f"Off to Bright: {ClockLightState.OFF - ClockLightState.BRIGHT}")
#     print(f"Off to Medium: {ClockLightState.OFF - ClockLightState.MEDIUM}")
#     print(f"Off to Dull: {ClockLightState.OFF - ClockLightState.DULL}")
#     print(f"Off to Auto: {ClockLightState.OFF - ClockLightState.AUTO}")
