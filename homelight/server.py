from pywizlight import discovery

from scenarios import *


async def getlight() -> wizlight or None:
	_bulbs = await discovery.discover_lights("192.168.50.255")

	try:
		_bulb = _bulbs[0]
		return _bulb
	except IndexError:
		print("Bulb is not available")
		return None


async def main():
	"""bulb = await getlight()
	if bulb is None:
		return"""
	bulb = wizlight("192.168.50.233")

	while True:
		await wake(bulb)
		await getup(bulb)
		await work(bulb)
		await chill(bulb)
		await relax(bulb)
		await sleep(bulb)


if __name__ == "__main__":
	loop = asyncio.get_event_loop()
	loop.run_until_complete(main())
