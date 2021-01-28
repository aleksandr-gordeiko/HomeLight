import asyncio
from controllers.wizbulbcontroller import WizBulbController
from schedulereader import ScheduleReader
import sys
import json

from util import alert


async def main(config_path: str = "./config/config.json"):
	with open(config_path) as f:
		conf: dict = json.load(f)

	# TODO Add KeyError handling
	controller: WizBulbController = WizBulbController(conf["default_bulb_ip"], conf["broadcast_ip"])
	await controller.initialize()
	alert("Bulb initialized")

	schedule_reader: ScheduleReader = ScheduleReader(conf["schedule_config_path"])

	while True:
		schedule: dict[str: int] = schedule_reader.get_current_parameters()
		await controller.apply_config(schedule)
		alert("Bulb config updated")
		await asyncio.sleep(conf["update_period"])


if __name__ == '__main__':
	loop = asyncio.get_event_loop()

	if len(sys.argv) > 1:
		config: str = sys.argv[1]
		loop.run_until_complete(main(config))
	else:
		loop.run_until_complete(main())
