import asyncio
from pywizlight import wizlight, discovery
from pywizlight.bulb import PilotBuilder, PilotParser

from homelight.controllers.controller import Controller
from homelight.bulbsmemory import *


class WizBulbController(Controller):
	def __init__(self, broadcast_ip: str, bulbs_storage_path: str):
		self.bulb: wizlight or None = None
		self.broadcast_ip: str = broadcast_ip
		self.bulbs_storage_path = bulbs_storage_path
		self.written_params: dict[str: int] = None

	async def initialize(self) -> bool:
		known = known_bulb_ips(self.bulbs_storage_path, "wiz")
		while True:
			try:
				bulb = wizlight(next(known))
				if self.is_bulb_available(bulb):
					self.bulb = bulb
					return True
			except StopIteration:
				break

		self.bulb = await self.find_bulb()
		if not self.bulb:
			return False
		save_bulb(self.bulbs_storage_path, "wiz", self.bulb.ip)
		return True

	async def find_bulb(self) -> wizlight or None:
		bulbs = await discovery.discover_lights(self.broadcast_ip)
		try:
			bulb = bulbs[0]
			return bulb
		except IndexError:
			return None

	async def is_bulb_available(self, bulb: wizlight) -> bool:
		timeout = 2
		try:
			await asyncio.wait_for(bulb.updateState(), timeout)
			return True
		except asyncio.exceptions.CancelledError:
			return False
		except asyncio.exceptions.TimeoutError:
			return False

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
	controller: WizBulbController = WizBulbController("192.168.50.255", "bulbs.json")
	asyncio.run(controller.initialize())
	print(asyncio.run(controller.get_params()))
