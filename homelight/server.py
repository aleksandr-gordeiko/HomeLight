import asyncio
import json

from controller import Controller
from wizbulbcontroller import WizBulbController
from schedulereader import ScheduleReader
from util import *


async def main(config_path: str = "./config/config.json"):
	with open(absdir(config_path)) as f:
		conf: dict = json.load(f)

	if "update_period" not in conf:
		conf["update_period"] = 60
	if "broadcast_ip" not in conf:
		alert("Invalid config (no broadcast_ip), aborting")
		return

	if "controller" in conf:
		if conf["controller"] == "wiz":
			controller_class = WizBulbController
		else:
			alert("Invalid controller, aborting")
			return
	else:
		controller_class = WizBulbController

	controller: Controller = controller_class(
		conf["broadcast_ip"],
		conf["bulb_storage_path"])
	if not await controller.initialize():
		alert("Bulb not found, aborting")
		return

	alert("Bulb initialized")

	schedule_reader: ScheduleReader = ScheduleReader(conf["schedule_config_path"])

	await controller.start_phythm(schedule_reader, conf["update_period"])


if __name__ == '__main__':
	loop = asyncio.get_event_loop()

	if len(sys.argv) > 1:
		config: str = sys.argv[1]
		loop.run_until_complete(main(config))
	else:
		loop.run_until_complete(main())

# FIXME When the bulb is physically off, the script exits
# TODO Update config on-the-go, when the config file changes
# FIXME Fix bug with powering off when manually set to night lightss
# TODO Update docs
# TODO Add multiple bulbs support
