import asyncio
import json
from pywizlight.exceptions import WizLightTimeOutError

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

	while True:
		try:
			await controller.start_phythm(schedule_reader, conf["update_period"])
		except WizLightTimeOutError:
			await asyncio.sleep(conf["update_period"])


if __name__ == '__main__':
	loop = asyncio.get_event_loop()

	if len(sys.argv) > 1:
		config: str = sys.argv[1]
		loop.run_until_complete(main(config))
	else:
		loop.run_until_complete(main())
