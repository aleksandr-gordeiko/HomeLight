import asyncio
from wizbulbcontroller import WizBulbController
from configreader import ConfigReader

from util import alert


async def main():
	controller: WizBulbController = WizBulbController()
	await controller.initialize()
	alert("Bulb initialized")

	config_reader: ConfigReader = ConfigReader("./config/schedule.json")

	while True:
		config: dict[str: int] = config_reader.get_current_parameters()
		await controller.apply_config(config)
		alert("Bulb config updated")
		await asyncio.sleep(60)


if __name__ == "__main__":
	loop = asyncio.get_event_loop()
	loop.run_until_complete(main())
