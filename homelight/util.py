import sys


def alert(msg: str) -> None:
	print(msg, file=sys.stderr)
