import asyncio
from pywizlight import wizlight, discovery
from pywizlight.bulb import PilotBuilder, PilotParser
from pywizlight.exceptions import WizLightTimeOutError

from controller import Controller
from bulbsmemory import *


class WizBulbController(Controller):
	def __init__(self, broadcast_ip: str, bulbs_storage_path: str):
		self.bulb: wizlight or None = None
		self.broadcast_ip: str = broadcast_ip
		self.bulbs_storage_path = bulbs_storage_path
		self.written_params: tuple[dict[str: int], bool] or None = None

	async def initialize(self) -> bool:
		known = known_bulb_ips(self.bulbs_storage_path, "wiz")
		while True:
			try:
				bulb = wizlight(next(known))
				if await self.is_bulb_available(bulb):
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
		old_params = self.written_params
		self.written_params = await self.get_params()
		if old_params != self.written_params:
			alert("Config updated")

	def get_written_params(self) -> dict[str: int]:
		return self.written_params

	async def get_params(self) -> dict[str: int]:
		_state: PilotParser = await self.bulb.updateState()
		return ({
			"brightness": _state.get_brightness(),
			"temperature": _state.get_colortemp()
		}, self.bulb.status)

	async def is_in_rhythm(self) -> bool:
		await self.bulb.updateState()
		return self.bulb.state.get_scene() == "Rhythm"

	async def start_phythm(self, schedule_reader, update_period: int) -> None:
		was_in_rhythm_just_now: bool = False
		while True:
			try:
				in_rhythm: bool = await self.is_in_rhythm()
				if await self.get_params() != self.get_written_params():
					was_in_rhythm_just_now = False

				if in_rhythm or was_in_rhythm_just_now:
					was_in_rhythm_just_now = True
					await self.apply_config(schedule_reader.get_current_parameters())
			except WizLightTimeOutError:
				pass

			await asyncio.sleep(update_period)


if __name__ == '__main__':
	controller: WizBulbController = WizBulbController("192.168.50.255", "bulbs.json")
	asyncio.run(controller.initialize())
	print(controller.bulb.status)
	# print(asyncio.run(controller.bulb.getBulbConfig()))
