from pywizlight import wizlight, discovery
from pywizlight.bulb import PilotBuilder

from util import alert


class WizBulbController:
	def __init__(self, default_ip: str, broadcast_ip: str):
		self.bulb = None
		self.default_ip: str = default_ip
		self.broadcast_ip: str = broadcast_ip

	async def initialize(self):
		self.bulb = await self._getlight()
		if not self.bulb:
			alert("Bulb discovery failed, using standard IP address {}".format(self.default_ip))
			self.bulb = wizlight(self.default_ip)

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

	async def set_off(self):
		await self.bulb.turn_off()

	async def apply_config(self, config: dict[str: int]):
		await self.set_light(config["brightness"], config["temperature"])
