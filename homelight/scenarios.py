from pywizlight import wizlight
from pywizlight.bulb import PilotBuilder
from datetime import datetime, time
import asyncio


async def wake(bulb: wizlight):
	while datetime.now().time() < time(6):
		await asyncio.sleep(60)
	await bulb.turn_on(PilotBuilder(brightness=40, colortemp=2700))


async def getup(bulb: wizlight):
	while datetime.now().time() < time(7):
		await asyncio.sleep(60)
	await bulb.turn_on(PilotBuilder(brightness=160, colortemp=3100))


async def work(bulb: wizlight):
	while datetime.now().time() < time(8, 30):
		await asyncio.sleep(60)
	await bulb.turn_on(PilotBuilder(brightness=200, colortemp=4000))


async def chill(bulb: wizlight):
	while datetime.now().time() < time(18):
		await asyncio.sleep(60)
	await bulb.turn_on(PilotBuilder(brightness=160, colortemp=3500))


async def relax(bulb: wizlight):
	while datetime.now().time() < time(21, 30):
		await asyncio.sleep(60)
	await bulb.turn_on(PilotBuilder(brightness=10, colortemp=3000))


async def sleep(bulb: wizlight):
	while datetime.now().time() < time(23, 59):
		await asyncio.sleep(60)
	await bulb.turn_off()
