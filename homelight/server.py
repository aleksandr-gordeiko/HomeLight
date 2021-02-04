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

	was_in_rhythm_just_now: bool = False
	while True:
		in_rhythm: bool = await controller.is_in_rhythm()
		if await controller.get_params() != controller.get_written_params():
			was_in_rhythm_just_now = False

		if in_rhythm or was_in_rhythm_just_now:
			was_in_rhythm_just_now = True
			await controller.apply_config(schedule_reader.get_current_parameters())
			alert("Bulb config updated")

		await asyncio.sleep(conf["update_period"])


if __name__ == '__main__':
	loop = asyncio.get_event_loop()

	if len(sys.argv) > 1:
		config: str = sys.argv[1]
		loop.run_until_complete(main(config))
	else:
		loop.run_until_complete(main())

# TODO Add multiple bulbs support
# TODO Fix bug with powering off when manually set to night light
