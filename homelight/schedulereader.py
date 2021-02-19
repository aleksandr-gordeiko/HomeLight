import json
import datetime
from util import *
import copy


class ScheduleReader:
	def __init__(self, path: str):
		self.path: str = path
		self.config: dict[str, dict[str: int]] = self._read_schedule_file()
		self.times: list[list[int]] = self._get_times()
		self.first_time: list[int] = self._get_first_time()

	def _read_schedule_file(self) -> dict[str, dict[str: int]]:
		with open(absdir(self.path)) as f:
			return json.load(f)

	@staticmethod
	def _string_time_to_int_list(time: str) -> list[int]:
		hr, mn = time.split(":")
		return [int(hr), int(mn)]

	@staticmethod
	def _int_list_time_to_string(time: list[int]) -> str:
		return "{}:{}".format(time[0], f'{time[1]:02}')

	def _get_times(self) -> list[list[int]]:
		times: list = []
		for time in self.config.keys():
			times.append(self._string_time_to_int_list(time))
		times.sort()
		return times

	def _get_first_time(self) -> list[int]:
		keys: list[list[int]] = self._get_times()
		keys.sort()
		return keys[0]

	def get_current_parameters(self) -> dict[str: int]:
		current_time: datetime.time = datetime.datetime.now().time()
		hours: int = current_time.hour
		minutes: int = current_time.minute
		curtime = [hours, minutes]

		temp = copy.deepcopy(self.times)
		temp.append(curtime)
		temp.sort()

		pos = temp.index(curtime)
		return self.config[self._int_list_time_to_string(self.times[pos-1])]
