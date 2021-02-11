import abc


class Controller(abc.ABC):
	@abc.abstractmethod
	async def initialize(self) -> bool:
		pass

	@abc.abstractmethod
	async def is_bulb_available(self, bulb) -> bool:
		pass

	@abc.abstractmethod
	async def set_light(self, brightness: int, temperature: int) -> None:
		pass

	@abc.abstractmethod
	async def set_off(self) -> None:
		pass

	@abc.abstractmethod
	async def apply_config(self, config: dict[str: int]) -> None:
		pass

	@abc.abstractmethod
	async def get_params(self) -> dict[str: int]:
		pass

	@abc.abstractmethod
	async def is_in_rhythm(self) -> bool:
		pass

	@abc.abstractmethod
	def get_written_params(self) -> dict[str: int]:
		pass

	@abc.abstractmethod
	async def start_phythm(self, schedule_reader, update_period: int) -> None:
		pass
