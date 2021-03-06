import json
from util import *


def known_bulb_ips(bulbs_path: str, bulb_type: str):
	try:
		with open(absdir(bulbs_path)) as cfg:
			config = json.load(cfg)
	except FileNotFoundError:
		return

	for bulb_ip in config[bulb_type]:
		yield bulb_ip


def save_bulb(bulbs_path: str, bulb_type: str, bulb_ip: str) -> None:
	try:
		with open(absdir(bulbs_path), "r+") as cfg:
			config = json.load(cfg)
			if bulb_ip in config[bulb_type]:
				return
			try:
				config[bulb_type].append(bulb_ip)
			except KeyError:
				config[bulb_type] = [bulb_ip]
			json.dump(config, cfg, indent=4)

	except FileNotFoundError:
		with open(absdir(bulbs_path), "w") as cfg:
			config = {bulb_type: [bulb_ip]}
			json.dump(config, cfg, indent=4)
