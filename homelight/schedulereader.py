import json
import datetime
from util import *


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
		if time.find(":") == -1:
			return [int(time), 0]
		else:
			hr, mn = time.split(":")
			return [int(hr), int(mn)]

	@staticmethod
	def _int_list_time_to_string(time: list[int]) -> str:
		if time[1] == 0:
			return str(time[0])
		else:
			return "{}:{}".format(time[0], time[1])

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

		actual_time: list[int] = self.first_time
		for time in self.times:
			if (time[0] > hours) or (time[0] == hours and time[1] >= minutes):
				if self.times.index(actual_time) == 0:
					return self.config[self._int_list_time_to_string(self.times[-1])]
				return self.config[self._int_list_time_to_string(actual_time)]
			actual_time = time
