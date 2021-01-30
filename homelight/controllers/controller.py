import abc


class Controller(abc.ABC):
	@abc.abstractmethod
	async def initialize(self) -> bool:
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

	async def is_params_changed(self):
		params: dict[str: int] = await self.get_params()
		while True:
			new_params: dict[str: int] = await self.get_params()
			if new_params == params:
				yield False
			else:
				params = new_params
				yield True
