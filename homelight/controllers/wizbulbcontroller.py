import asyncio
from pywizlight import wizlight, discovery
from pywizlight.bulb import PilotBuilder, PilotParser

from homelight.controllers.controller import Controller
from homelight.util import alert
from homelight.bulbsmemory import *


class WizBulbController(Controller):
	def __init__(self, default_ip: str, broadcast_ip: str, bulbs_storage_path: str):
		self.bulb: wizlight or None = None
		self.default_ip: str = default_ip
		self.broadcast_ip: str = broadcast_ip
		self.bulbs_storage_path = bulbs_storage_path
		self.written_params: dict[str: int] = None

	async def initialize(self) -> bool:
		known = known_bulbs(self.bulbs_storage_path, "wiz")
		while True:
			try:
				self.bulb = wizlight(next(known))
				return True
			except StopIteration:
				break

		self.bulb = await self._getlight()
		if not self.bulb:
			if self.default_ip:
				alert("Bulb discovery failed, using default IP address {}".format(self.default_ip))
				self.bulb = wizlight(self.default_ip)
				save_bulb(self.bulbs_storage_path, "wiz", self.bulb.ip)
				return True
			return False
		save_bulb(self.bulbs_storage_path, "wiz", self.bulb.ip)
		return True

	async def _getlight(self) -> wizlight or None:
		bulbs = await discovery.discover_lights(self.broadcast_ip)
		try:
			bulb = bulbs[0]
			return bulb
		except IndexError:
			return None

	async def set_light(self, brightness: int, temperature: int) -> None:
		if brightness == 0:
			await self.set_off()
		else:
			await self.bulb.turn_on(PilotBuilder(brightness=brightness, colortemp=temperature))

	async def set_off(self) -> None:
		await self.bulb.turn_off()

	async def apply_config(self, config: dict[str: int]) -> None:
		await self.set_light(config["brightness"], config["temperature"])
		self.written_params = await self.get_params()

	def get_written_params(self) -> dict[str: int]:
		return self.written_params

	async def get_params(self) -> dict[str: int]:
		_state: PilotParser = await self.bulb.updateState()
		return {
			"brightness": _state.get_brightness(),
			"temperature": _state.get_colortemp()
		}

	async def is_in_rhythm(self) -> bool:
		await self.bulb.updateState()
		return self.bulb.state.get_scene() == "Rhythm"


if __name__ == '__main__':
	controller: WizBulbController = WizBulbController("192.168.50.99", "192.168.50.255", "bulbs.json")
	asyncio.run(controller.initialize())
	print(asyncio.run(controller.get_params()))
