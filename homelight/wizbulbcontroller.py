from pywizlight import wizlight, discovery
from pywizlight.bulb import PilotBuilder

from util import alert


class WizBulbController:
	def __init__(self):
		self.bulb = None

	async def initialize(self):
		self.bulb = await self._getlight()
		if not self.bulb:
			alert("Bulb discovery failed, using standard IP address 192.168.50.233")
			self.bulb = wizlight("192.168.50.233")

	@staticmethod
	async def _getlight() -> wizlight or None:
		bulbs = await discovery.discover_lights("192.168.50.255")
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

	async def set_off(self):
		await self.bulb.turn_off()

	async def apply_config(self, config: dict[str: int]):
		await self.set_light(config["brightness"], config["temperature"])
