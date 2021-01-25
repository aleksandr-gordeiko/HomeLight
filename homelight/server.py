import asyncio
from pywizlight import discovery, wizlight
from pywizlight.bulb import PilotBuilder


async def getlight() -> wizlight or None:
	_bulbs = await discovery.discover_lights("192.168.50.255")

	try:
		_bulb = _bulbs[0]
		return _bulb
	except IndexError:
		print("Bulb is not available")
		return None


async def blink(bulb: wizlight):
	await bulb.turn_off()
	await bulb.turn_on()


async def main():
	bulb = wizlight("192.168.50.233")

	await blink(bulb)


if __name__ == "__main__":
	loop = asyncio.get_event_loop()
	loop.run_until_complete(main())
