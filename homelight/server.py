import asyncio
from wizbulbcontroller import WizBulbController
from configreader import ConfigReader

from util import alert


async def main(
		config_path: str = "./config/schedule.json",
		broadcast_ip: str = "192.168.50.255",
		default_ip: str = "192.168.50.233",
		update_peroid_sec: int = 60
):
	controller: WizBulbController = WizBulbController(default_ip, broadcast_ip)
	await controller.initialize()
	alert("Bulb initialized")

	config_reader: ConfigReader = ConfigReader(config_path)

	while True:
		config: dict[str: int] = config_reader.get_current_parameters()
		await controller.apply_config(config)
		alert("Bulb config updated")
		await asyncio.sleep(update_peroid_sec)


def run(
		config_path: str = "./config/schedule.json",
		broadcast_ip: str = "192.168.50.255",
		default_ip: str = "192.168.50.233",
		update_peroid_sec: int = 60
):
	loop = asyncio.get_event_loop()
	loop.run_until_complete(main(config_path, broadcast_ip, default_ip, update_peroid_sec))


if __name__ == '__main__':
	run()
