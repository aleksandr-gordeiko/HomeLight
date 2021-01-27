from pywizlight import wizlight
from pywizlight.bulb import PilotBuilder


class WizBulbController:

	def __init__(self):
		self.bulb: wizlight = await self._getlight()

	@staticmethod
	async def _getlight() -> wizlight:
		return wizlight("192.168.50.233")

	async def set_light(self, brightness: int, temperature: int) -> None:
		if brightness == 0:
			await self.set_off()
		else:
			await self.bulb.turn_on(PilotBuilder(brightness=brightness, colortemp=temperature))

	async def set_off(self):
		await self.bulb.turn_off()

	async def apply_config(self, config: dict[str: int]):
		await self.set_light(config["brightness"], config["temperature"])
