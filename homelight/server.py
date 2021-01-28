import asyncio
from controllers.wizbulbcontroller import WizBulbController
from schedulereader import ScheduleReader
import sys
import json

from util import alert


async def main(config_path: str = "./config/config.json"):
	with open(config_path) as f:
		conf: dict = json.load(f)

	if "update_period" not in conf:
		conf["update_period"] = 60
	if "default_bulb_ip" not in conf:
		conf["default_bulb_ip"] = None
	if "broadcast_ip" not in conf:
		alert("Invalid config (no broadcast_ip), exitting")
		return

	controller: WizBulbController = WizBulbController(conf["default_bulb_ip"], conf["broadcast_ip"])
	if not await controller.initialize():
		alert("Bulb not found, exitting")
		return

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

# TODO Add bulb parameter check: if does not fit the schedule, restore
