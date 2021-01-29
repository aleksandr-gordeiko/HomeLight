import abc


class ControllerInterface(abc.ABC):
	@abc.abstractmethod
	async def initialize(self) -> bool:
		pass

	@abc.abstractmethod
	async def set_light(self, brightness: int, temperature: int) -> None:
		pass

	@abc.abstractmethod
	async def set_off(self):
		pass

	@abc.abstractmethod
	async def apply_config(self, config: dict[str: int]):
		pass
